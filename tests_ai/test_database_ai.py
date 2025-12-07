
import unittest
import sqlite3
from database import Database

class TestDatabaseAI(unittest.TestCase):

    def setUp(self):
        # Use an in-memory database for testing
        self.db = Database(":memory:")
        self.db.add_customer("John", "Doe", "M", 30, "New York", "Google")
        self.db.add_customer("Jane", "Smith", "F", 28, "London", "Apple")
        self.db.add_customer("Peter", "Jones", "M", 45, "Sydney", "Amazon")

    def test_view_customers_sorted(self):
        # Test sorting by name in ascending order
        customers = self.db.view_customers_sorted("name", "ASC")
        self.assertEqual(customers[0][1], "Jane")
        self.assertEqual(customers[1][1], "John")
        self.assertEqual(customers[2][1], "Peter")

        # Test sorting by age in descending order
        customers = self.db.view_customers_sorted("age", "DESC")
        self.assertEqual(customers[0][4], 45)
        self.assertEqual(customers[1][4], 30)
        self.assertEqual(customers[2][4], 28)

    def test_search_customers(self):
        # Test search by name
        customers = self.db.search_customers("John")
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0][1], "John")

        # Test search by surname
        customers = self.db.search_customers("Smith")
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0][2], "Smith")

        # Test search by company
        customers = self.db.search_customers("Amazon")
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0][6], "Amazon")

        # Test search with no results
        customers = self.db.search_customers("Microsoft")
        self.assertEqual(len(customers), 0)

    def test_add_customer_details(self):
        self.db.add_customer("Alice", "Wonderland", "F", 25, "New York", "Microsoft")
        customers = self.db.search_customers("Alice")
        self.assertEqual(len(customers), 1)
        customer = customers[0]
        self.assertEqual(customer[1], "Alice")
        self.assertEqual(customer[2], "Wonderland")
        self.assertEqual(customer[3], "F")
        self.assertEqual(customer[4], 25)
        self.assertEqual(customer[5], "New York")
        self.assertEqual(customer[6], "Microsoft")

    def tearDown(self):
        # The in-memory database is automatically discarded
        pass

if __name__ == '__main__':
    unittest.main()
