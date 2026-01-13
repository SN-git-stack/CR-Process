# Architectural Standards & Rules

## 1. Allowed Tech Stack
- **Backend**: Python (FastAPI) or C# (.NET Core). **NO JAVA**.
- **Frontend**: React (TypeScript).
- **Database**: PostgreSQL (Structured), Redis (Cache).

## 2. API Guidelines
- All APIs must be RESTful.
- Must include Swagger/OpenAPI documentation.
- Authentication via OAuth2 / JWT.

## 3. Offline Capabilities
- Crucial: The POS MUST function 100% offline for core sales.
- Sync mechanism: Store-and-forward pattern using local SQLite DB.
