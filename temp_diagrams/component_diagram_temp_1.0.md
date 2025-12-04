```mermaid
graph TD;
    subgraph "main"
        A[main.py]
    end

    subgraph "GUI"
        B[App]
        B_methods(
            __init__(db)
            populate_list()
            add_customer()
            select_customer(event)
            update_customer()
            delete_customer()
            clear_fields()
        )
        B --> B_methods
    end

    subgraph "Database"
        C[Database]
        C_methods(
            __init__(db_file)
            create_table()
            add_customer()
            view_customers()
            update_customer()
            delete_customer()
        )
        C --> C_methods
        D[(customers.db)]
    end

    A --> B
    A --> C
    B --> C
    C --> D
```
