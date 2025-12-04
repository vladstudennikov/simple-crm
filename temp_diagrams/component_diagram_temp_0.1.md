```mermaid
graph TD;
    A[main.py] --> B(gui.py);
    A --> C(database.py);
    B --> C;
```