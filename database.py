import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT,
                patronymic TEXT,
                age INTEGER,
                city TEXT,
                company TEXT
            )
        """)
        self.conn.commit()

    def add_customer(self, name, surname, patronymic, age, city, company):
        self.cur.execute("INSERT INTO customers (name, surname, patronymic, age, city, company) VALUES (?, ?, ?, ?, ?, ?)",
                         (name, surname, patronymic, age, city, company))
        self.conn.commit()

    def view_customers(self):
        self.cur.execute("SELECT * FROM customers")
        return self.cur.fetchall()

    def view_customers_sorted(self, column, order):
        self.cur.execute(f"SELECT * FROM customers ORDER BY {column} {order}")
        return self.cur.fetchall()

    def search_customers(self, text):
        self.cur.execute("SELECT * FROM customers WHERE name LIKE ? OR surname LIKE ? OR company LIKE ?",
                         (f"%{text}%", f"%{text}%", f"%{text}%"))
        return self.cur.fetchall()

    def update_customer(self, customer_id, name, surname, patronymic, age, city, company):
        self.cur.execute("""
            UPDATE customers SET name = ?, surname = ?, patronymic = ?, age = ?, city = ?, company = ?
            WHERE id = ?
        """, (name, surname, patronymic, age, city, company, customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        self.cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()