# Multipath Dishware Integration Description

**Target System**: TCPOS (Zucchetti)
**Tech Stack**: C# .NET 10, MSSQL (Server), SQLite (Local), WPF

## 1. Architectural Overview

The **Multipath Dishware Integration** introduces a generic middleware layer (`DishwareService`) into the TCPOS Core. This service acts as a facade, decoupling the Point of Sale logic from specific reusable packaging providers (Relevo, Vytal, Recup).

### Core Components

1.  **TCPOS.Plugins.Dishware**: The main plugin assembly.
2.  **IReusablePackagingProvider**: The standard interface for all providers.
3.  **DishwareService**: Singleton service managing the active provider and offline queue.
4.  **Local Worker**: Background thread for processing the offline `RentalQueue`.

## 2. Interface Definition

Located in `TCPOS.Plugins.Interfaces`.

```csharp
public interface IReusablePackagingProvider
{
    /// <summary>
    /// Unique identifier for the provider (e.g., "RELEVO", "VYTAL").
    /// </summary>
    string ProviderId { get; }

    /// <summary>
    /// Validates a scanned item UID with the backend.
    /// </summary>
    Task<DishwareItemStatus> CheckStatusAsync(string itemUid);

    /// <summary>
    /// Confirms the rental/deposit of the item.
    /// </summary>
    Task<TransactionResult> ConfirmLeaseAsync(string itemUid, string transactionId);
    
    /// <summary>
    /// Confirms the return of an item (if supported at POS).
    /// </summary>
    Task<TransactionResult> ConfirmReturnAsync(string itemUid, string transactionId);
}
```

## 3. Data Model

### Server Database (MSSQL)

**Table**: `Dishware_ProviderConfig`
| Column | Type | Description |
| :--- | :--- | :--- |
| `ProviderID` | NVARCHAR(50) | PK, e.g., 'RELEVO' |
| `ApiKey` | VARBINARY | Encrypted API Key |
| `ApiEndpoint` | NVARCHAR(255) | Base URL |
| `IsActive` | BIT | 1 = Enabled |
| `ConfigJson` | NVARCHAR(MAX) | Provider-specific settings |

### Local Database (SQLite)

**Table**: `Dishware_RentalQueue`
| Column | Type | Description |
| :--- | :--- | :--- |
| `QueueId` | GUID | PK |
| `CreatedAt` | DATETIME | Timestamp |
| `ProviderId` | NVARCHAR(50) | Target Provider |
| `ActionType` | INT | 1=Check, 2=Lease, 3=Return |
| `PayloadJson` | TEXT | Serialized request data |
| `RetryCount` | INT | Number of failed attempts |

## 4. Relevo Implementation Details

The `RelevoProvider` implements `IReusablePackagingProvider`.

*   **Authentication**: Uses `x-api-key` header.
*   **HTTP Client**: Injected via `IHttpClientFactory`.
*   **Endpoints**:
    *   GET `/v1/items/{uid}` (Check Status)
    *   POST `/v1/transactions/lease` (Confirm Lease)

## 5. Offline & Sync Logic

1.  **Online Mode**: `DishwareService` calls `provider.ConfirmLeaseAsync()`. If successful, the transaction completes.
2.  **Offline Mode / Timeout**:
    *   If API call fails (Timeout or 5xx), the request is serialized and saved to `Dishware_RentalQueue` (SQLite).
    *   POS Transaction continues (Optimistic Offline Mode).
    *   User sees a warning: *"Offline - Transaction queued"*.
3.  **Sync Worker**:
    *   Runs every 60 seconds.
    *   Reads `Dishware_RentalQueue`.
    *   Retries the request.
    *   On success -> deletes row.
    *   On fatal error (400 Bad Request) -> moves to `Dishware_DeadLetterQueue` and alerts admin.

## 6. Security

*   **API Keys**: Never stored in plain text. Encrypted using DPAPI (Local) or TCPOS Encryption Utils (Server).
*   **Logs**: All actions logged to `Dishware_Log` (Audit Trail), explicitly excluding PII from the log message.
