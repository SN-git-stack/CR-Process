# Diskussionspapier: Architekturstrategien zur Integration mehrerer Anbieter

**Datum**: 14.01.2026
**Thema**: Integration externer Liefer- und Serviceanbieter (z.B. UberEats, Lieferando, Payment-Provider)
**Ziel**: Vergleich verschiedener Architekturansätze zur Vorbereitung auf das Gespräch mit dem Systemarchitekten.

## 1. Ausgangslage
Wir müssen eine Vielzahl heterogener Drittanbieter in unser POS-System integrieren. Unser Architekt bevorzugt aktuell einen Ansatz basierend auf **API Gateway** und **Docker**-Containern. Dieses Dokument beleuchtet diesen Ansatz sowie Alternativen, um eine fundierte Entscheidung zu treffen.

---

## 2. Option A: Zentrales API Gateway mit Microservices (Favorit)
Jeder Anbieter-Adapter läuft als isolierter Docker-Container. Ein zentrales Gateway (z.B. Kong, Tyk oder Azure API Management) routet die Anfragen und kümmert sich um Authentifizierung und Rate-Limiting.

### Vorteile (Pros)
*   **Isolation**: Wenn der "UberEats-Container" abstürzt, läuft das restliche System weiter.
*   **Skalierbarkeit**: Stark frequentierte Adapter können unabhängig skaliert werden.
*   **Standardisierung**: Das Gateway erzwingt einheitliche Sicherheitsrichtlinien (z.B. OAuth2) für alle eingehenden Webhooks.
*   **Tech-Stack Flexibilität**: Ein Adapter kann in Python, ein anderer in Go geschrieben sein, solange sie Dockerisierte HTTP-Services sind.

### Nachteile (Cons)
*   **Komplexität**: Erfordert Orchestrierung (Kubernetes/Docker Swarm) und erhöht den Ops-Aufwand.
*   **Latenz**: Ein zusätzlicher Hop durch das Gateway.
*   **Kosten**: Höherer Ressourcenverbrauch durch viele separate Container für kleine Integrationen.

---

## 3. Option B: Modulith (Modularer Monolith) mit Adapter-Pattern
Die Integrationen sind als Module (Bibliotheken) direkt in den Core-Backend-Service eingebunden. Es gibt keine Netzwerk-Grenze zwischen Core und Adapter.

### Vorteile (Pros)
*   **Einfachheit**: Deployment eines einzigen Artefakts. Kein komplexes Container-Management nötig.
*   **Performance**: Keine Netzwerk-Latenz zwischen Core und Adapter (In-Process Calls).
*   **Debugging**: Einfacheres Tracing, da alles in einem Prozess passiert.

### Nachteile (Cons)
*   **Resilienz-Risiko**: Ein Speicherleck im "Lieferando-Modul" reißt den gesamten POS-Server mit.
*   **Abhängigkeitshölle**: Konfligierende Libraries (z.B. verschiedene `requests` Versionen) können schwer lösbar sein.
*   **Release-Zyklus**: Ein Fix für einen kleinen Adapter erfordert ein Redeployment des gesamten Monolithen.

---

## 4. Option C: Event-Driven Architecture (Asynchron)
Provider-Adapter empfangen Events (Webhooks) und schreiben standardisierte "Bestell-Events" in eine Message Queue (z.B. Kafka, RabbitMQ). Der Core konsumiert diese asynchron.

### Vorteile (Pros)
*   **Spitzenglättung (Traffic Bursts)**: Hohe Last (z.B. Silvesterabend) wird gepuffert. Der Core stürzt nicht ab, sondern arbeitet die Queue ab.
*   **Entkopplung**: Sender und Empfänger müssen nicht gleichzeitig online sein.

### Nachteile (Cons)
*   **Komplexität**: Einführung einer Message-Broker-Infrastruktur.
*   **Fehlerbehandlung**: Was passiert bei "Dead Letters"? Debugging von asynchronen Flows ist schwerer.
*   **Overhead**: Für einfache synchrone Abfragen (z.B. "Ist Artikel X verfügbar?") oft Overkill.

---

## 5. Empfehlung für die Diskussion
Da der Architekt **API Gateway & Docker** bevorzugt, sollten wir **Option A** als Basis nutzen, aber folgende Punkte challengen:

1.  **Overhead für kleine Adapter**: Lohnt sich ein eigener Container für einen Provider mit <10 Calls pro Tag? -> *Vorschlag: Ein "Shared Adapter Service" für Long-Tail-Anbieter.*
2.  **Latenz**: Ist das Gateway performant genug für synchrone Bestätigungen (z.B. Payment)?
3.  **Kosten**: Wie halten wir die Cloud-Kosten im Rahmen, wenn wir 50+ Container laufen haben?

**Fazit**: Option A ist zukunftssicher, aber wir müssen aufpassen, dass wir nicht "Over-Engineering" betreiben.
