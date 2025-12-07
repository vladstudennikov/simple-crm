
import unittest
import sqlite3
from database import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Use an in-memory database for testing
        self.db = Database(":memory:")

    def test_add_and_view_customer(self):
        self.db.add_customer("John", "Doe", "M", 30, "New York", "Google")
        customers = self.db.view_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0][1], "John")

    def test_update_customer(self):
        self.db.add_customer("Jane", "Doe", "F", 28, "London", "Apple")
        customer_id = self.db.view_customers()[0][0]
        self.db.update_customer(customer_id, "Jane", "Smith", "F", 29, "Paris", "Microsoft")
        customers = self.db.view_customers()
        self.assertEqual(customers[0][2], "Smith")
        self.assertEqual(customers[0][4], 29)

    def test_delete_customer(self):
        self.db.add_customer("Peter", "Jones", "M", 45, "Sydney", "Amazon")
        customer_id = self.db.view_customers()[0][0]
        self.db.delete_customer(customer_id)
        customers = self.db.view_customers()
        self.assertEqual(len(customers), 0)

    def tearDown(self):
        # The in-memory database is automatically discarded
        pass

if __name__ == '__main__':
    unittest.main()
