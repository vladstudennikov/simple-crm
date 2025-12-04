# Project Documentation: Simple CRM

## 1. Introduction

This document provides a detailed overview of the Simple CRM application, including its requirements, stakeholders, and architecture. The project is a standalone desktop application designed to help small businesses or individuals manage customer contact information efficiently.

### 1.1 Purpose

The primary purpose of this application is to provide a simple, user-friendly tool for storing and managing customer data locally. It replaces the need for manual records or complex, web-based CRM systems for users with basic contact management needs.

### 1.2 Scope

The application is a single-user desktop program. Its scope is limited to core contact management functionalities: creating, reading, updating, and deleting customer records. All data is stored in a local SQLite database file.

---

## 2. Business Requirements

### 2.1 High-Level Goals

- **BR-1:** Provide a centralized and persistent storage for customer contact details.
- **BR-2:** Enable users to easily manage their customer list without requiring an internet connection.
- **BR-3:** Offer a clean and intuitive graphical user interface to minimize the learning curve.

---

## 3. Stakeholders

| Role          | Description                                                                 | Interest                                                               |
|---------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------|
| **End-User**  | The primary user of the application (e.g., small business owner, freelancer). | A functional, reliable, and easy-to-use tool for managing contacts.      |
| **Developer** | The individual or team responsible for building and maintaining the software. | A clear set of requirements and well-defined architecture.             |

---

## 4. Functional Requirements

The system shall allow the user to perform the following actions:

| ID      | Requirement                                                                      |
|---------|----------------------------------------------------------------------------------|
| **FR-1**  | **Add a Customer:** The user shall be able to add a new customer record with a name, surname, age, city and company. |
| **FR-2**  | **View Customers:** The user shall be able to see a complete list of all saved customer records. |
| **FR-3**  | **Update a Customer:** The user shall be able to select an existing customer from the list and modify their details. |
| **FR-4**  | **Delete a Customer:** The user shall be able to select an existing customer from the list and permanently remove their record. |
| **FR-5**  | **Select a Customer:** The user shall be able to click on a customer in the list to populate the entry fields with that customer's current details. |

---

## 5. Non-Functional Requirements

| ID      | Category      | Requirement                                                                                                   |
|---------|---------------|---------------------------------------------------------------------------------------------------------------|
| **NFR-1** | **Usability**   | The graphical user interface (GUI) must be intuitive and require minimal training for a non-technical user. |
| **NFR-2** | **Performance** | The application should load quickly and display the customer list with minimal delay.                         |
| **NFR-3** | **Reliability** | The application must ensure that data is saved correctly and is not lost between sessions.                    |
| **NFR-4** | **Platform**    | The application must run on common desktop operating systems (Windows, macOS, Linux) where Python is supported. |
| **NFR-5** | **Storage**     | The application must store all user data in a single, portable database file (`customers.db`).                |
| **NFR-6** | **Dependencies**| The application should rely only on Python's standard libraries to avoid complex installation procedures.   |

---

## 6. System Architecture

The application follows a simple 2-tier architecture.

### 6.1 Presentation Layer

- **File:** `gui_qt.py`
- **Description:** This layer is built using Python's native `PyQt` library. It is responsible for rendering the user interface, capturing all user input (button clicks, text entry), and displaying customer data. It communicates directly with the Data Layer to perform actions.

### 6.2 Data Layer

- **File:** `database.py`
- **Description:** This layer provides an abstraction over the physical database. It uses the `sqlite3` library to execute SQL commands for all CRUD (Create, Read, Update, Delete) operations. It is responsible for creating the database table and managing all data persistence.

### 6.3 Application Entry Point

- **File:** `main.py`
- **Description:** This script initializes the Data Layer (`Database` class) and the Presentation Layer (`App` class) and starts the main application event loop, making it the executable entry point.

---

## 7. Data Model

The application uses a single table in an SQLite database to store customer information.

- **Database File:** `customers.db`
- **Table Name:** `customers`

### 7.1 `customers` Table Schema

| Column Name | Data Type       | Constraints        | Description                                  |
|-------------|-----------------|--------------------|----------------------------------------------|
| `id`        | `INTEGER`       | `PRIMARY KEY`      | A unique identifier for each customer record.|
| `name`      | `TEXT`          | `NOT NULL`         | The full name of the customer.               |
| `surname`      | `TEXT`          |                    | The surname of the customer.           |
| `age`     | `INTEGER`          |                    | The age of the customer.           |
| `city`     | `TEXT`          |                    | The city of the customer.           |
| `company`     | `TEXT`          |                    | The company of the customer.            |
