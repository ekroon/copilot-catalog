# Mermaid Diagram Types — GitHub-Compatible Syntax Reference

## Flowchart

```mermaid
flowchart TD
    A["Rectangle"] --> B(["Stadium/Rounded"])
    B --> C{"Decision"}
    C -->|"Yes"| D[("Database/Cylinder")]
    C -->|"No"| E(("Circle"))
```

### Node Shapes
- `["Text"]` — Rectangle (most common)
- `(["Text"])` — Stadium/rounded (start/end/users)
- `{"Text"}` — Diamond/rhombus (decisions)
- `[("Text")]` — Cylinder (databases)
- `(("Text"))` — Circle (events)
- `[["Text"]]` — Subroutine (double border)

### Edge Types
- `-->` — Solid arrow
- `---` — Solid line (no arrow)
- `-.->` — Dotted arrow
- `-. "text" .->` — Dotted arrow with label
- `==>` — Thick arrow
- `-- "text" -->` — Arrow with label
- `-->|"text"|` — Arrow with label (alt syntax)

### Direction
- `TD` / `TB` — Top to bottom (best for hierarchical)
- `LR` — Left to right (best for pipelines)
- `RL` — Right to left
- `BT` — Bottom to top

### Subgraphs
```mermaid
flowchart TD
    subgraph GroupName["Display Name"]
        A --> B
    end
    subgraph AnotherGroup["Another Group"]
        direction LR
        C --> D
    end
    B --> C
```

Use `direction LR` inside a subgraph to override the parent direction.

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database

    C->>S: Request
    activate S
    S->>DB: Query
    activate DB
    DB-->>S: Result
    deactivate DB
    S-->>C: Response
    deactivate S

    Note over C,S: This is a note
```

### Arrow Types
- `->>` — Solid arrow (request)
- `-->>` — Dashed arrow (response)
- `-x` — Cross (failed)
- `-)` — Async

### Grouping
- `rect rgb(200, 220, 255)` ... `end` — Highlighted region
- `loop Label` ... `end` — Loop
- `alt Label` ... `else Label` ... `end` — Conditional
- `opt Label` ... `end` — Optional

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start
    Processing --> Done: complete
    Processing --> Error: fail
    Error --> Idle: retry
    Done --> [*]
```

### Composite States
```mermaid
stateDiagram-v2
    state Active {
        [*] --> Running
        Running --> Paused: pause
        Paused --> Running: resume
    }
```

---

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +fetch() void
    }
    Animal <|-- Dog
```

### Relationships
- `<|--` — Inheritance
- `*--` — Composition
- `o--` — Aggregation
- `-->` — Association
- `..>` — Dependency
- `..|>` — Realization

---

## ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "is in"
```

### Cardinality
- `||` — Exactly one
- `o|` — Zero or one
- `}|` — One or more
- `}o` — Zero or more
