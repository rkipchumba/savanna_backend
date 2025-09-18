┌─────────────┐
│   Customer  │
│─────────────│
│ id (PK)     │
│ user_id (FK)│ ──┐
│ phone       │   │
└─────────────┘   │
                  │
                  │
                  │
           ┌──────▼───────┐
           │    Order     │
           │─────────────│
           │ id (PK)     │
           │ customer_id │
           │ total_price │
           │ created_at  │
           └─────────────┘
                  │
                  │ Many-to-Many via OrderItem
                  │
           ┌──────▼───────┐
           │   Product    │
           │─────────────│
           │ id (PK)     │
           │ name        │
           │ price       │
           │ category_id │
           └─────────────┘
                  │
                  │ Many products belong to one category
                  │
           ┌──────▼───────┐
           │  Category    │
           │─────────────│
           │ id (PK)     │
           │ name        │
           │ parent_id   │ ──┐ (self-referencing for hierarchy)
           └─────────────┘   │
                             │
                             └── Arbitrary depth (All Products > Bakery > Bread > etc.)
