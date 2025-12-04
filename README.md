# Simple CRM Application

This is a simple desktop application for managing customer contacts, built with Python and Tkinter.

## Description

The application provides a graphical user interface to perform basic CRUD (Create, Read, Update, Delete) operations on a local customer database.

## Features

- Add new customers with name, email, and phone number.
- View a list of all existing customers.
- Update the information of a selected customer.
- Delete a customer from the database.

## How to Run

1.  Ensure you have Python 3 installed.
2.  Open a terminal or command prompt.
3.  Navigate to the project directory.
4.  Run the application with the following command:

    ```bash
    python main.py
    ```

## Project Structure

- `main.py`: The main entry point of the application.
- `gui.py`: Defines the user interface and application logic.
- `database.py`: Manages the SQLite database and data operations.
- `customers.db`: The SQLite database file where customer data is stored.
- `docs/`: Contains project documentation.
