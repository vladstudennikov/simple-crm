```mermaid
graph TD;
    subgraph "Entry Point"
        A[main.py]
    end

    subgraph "User Interface (tkinter)"
        B[App]
        B_widgets(
            - frame_left
            - frame_right
            - name_label, email_label, phone_label
            - name_entry, email_entry, phone_entry
            - add_btn, update_btn, delete_btn, clear_btn
            - customer_list, scrollbar
        )
        B_methods(
            + __init__(db)
            + populate_list()
            + add_customer()
            + select_customer(event)
            + update_customer()
            + delete_customer()
            + clear_fields()
        )
        B -- contains --> B_widgets
        B -- contains --> B_methods
        T[tk.Tk]
        T -- inherited by --> B
    end

    subgraph "Data Persistence (sqlite3)"
        C[Database]
        C_methods(
            + __init__(db_file)
            - create_table()
            + add_customer()
            + view_customers()
            + update_customer()
            + delete_customer()
            - __del__()
        )
        C_conn(
            - conn
            - cur
        )
        C -- contains --> C_methods
        C -- contains --> C_conn
        S[sqlite3]
        S -- used by --> C
        D[(customers.db)]
    end

    A -- instantiates --> B
    A -- instantiates --> C
    B -- calls --> C
    C -- interacts with --> D
```