import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QFileDialog
)
import csv
from database import Database

class App(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_sort_column = 0
        self.current_sort_order = 'ASC'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Modern CRM')
        self.setGeometry(100, 100, 1200, 600)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Left panel for input fields
        left_panel = QVBoxLayout()

        # Labels and Line Edits
        self.name_label = QLabel('Name:')
        self.name_input = QLineEdit()
        self.surname_label = QLabel('Surname:')
        self.surname_input = QLineEdit()
        self.patronymic_label = QLabel('Patronymic:')
        self.patronymic_input = QLineEdit()
        self.age_label = QLabel('Age:')
        self.age_input = QLineEdit()
        self.city_label = QLabel('City:')
        self.city_input = QLineEdit()
        self.company_label = QLabel('Company:')
        self.company_input = QLineEdit()

        left_panel.addWidget(self.name_label)
        left_panel.addWidget(self.name_input)
        left_panel.addWidget(self.surname_label)
        left_panel.addWidget(self.surname_input)
        left_panel.addWidget(self.patronymic_label)
        left_panel.addWidget(self.patronymic_input)
        left_panel.addWidget(self.age_label)
        left_panel.addWidget(self.age_input)
        left_panel.addWidget(self.city_label)
        left_panel.addWidget(self.city_input)
        left_panel.addWidget(self.company_label)
        left_panel.addWidget(self.company_input)

        # Buttons
        self.add_btn = QPushButton('Add Customer')
        self.add_btn.clicked.connect(self.add_customer)
        self.update_btn = QPushButton('Update Selected')
        self.update_btn.clicked.connect(self.update_customer)
        self.delete_btn = QPushButton('Delete Selected')
        self.delete_btn.clicked.connect(self.delete_customer)
        self.clear_btn = QPushButton('Clear Fields')
        self.clear_btn.clicked.connect(self.clear_fields)
        self.export_btn = QPushButton('Export to CSV')
        self.export_btn.clicked.connect(self.export_to_csv)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.export_btn)
        left_panel.addLayout(button_layout)

        # Right panel for the table
        right_panel = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, surname, or company")
        self.search_input.textChanged.connect(self.search_customers)
        search_layout.addWidget(self.search_input)
        right_panel.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Surname', 'Patronymic', 'Age', 'City', 'Company'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.table.itemClicked.connect(self.select_customer)
        right_panel.addWidget(self.table)

        main_layout.addLayout(left_panel)
        main_layout.addLayout(right_panel)

        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(0)
        column_names = ['id', 'name', 'surname', 'patronymic', 'age', 'city', 'company']
        sort_column_name = column_names[self.current_sort_column]
        
        for row_data in self.db.view_customers_sorted(sort_column_name, self.current_sort_order):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, data in enumerate(row_data):
                self.table.setItem(row_position, col, QTableWidgetItem(str(data)))

    def sort_table(self, logicalIndex):
        if logicalIndex == self.current_sort_column:
            self.current_sort_order = 'DESC' if self.current_sort_order == 'ASC' else 'ASC'
        else:
            self.current_sort_column = logicalIndex
            self.current_sort_order = 'ASC'
        self.populate_table()

    def add_customer(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        patronymic = self.patronymic_input.text()
        age = self.age_input.text()
        city = self.city_input.text()
        company = self.company_input.text()

        if name:
            try:
                age = int(age)
                self.db.add_customer(name, surname, patronymic, age, city, company)
                self.populate_table()
                self.clear_fields()
            except ValueError:
                QMessageBox.critical(self, 'Error', 'Age must be a number.')
        else:
            QMessageBox.critical(self, 'Error', 'Name field cannot be empty.')

    def select_customer(self, item):
        row = item.row()
        self.selected_item_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text())
        self.surname_input.setText(self.table.item(row, 2).text())
        self.patronymic_input.setText(self.table.item(row, 3).text())
        self.age_input.setText(self.table.item(row, 4).text())
        self.city_input.setText(self.table.item(row, 5).text())
        self.company_input.setText(self.table.item(row, 6).text())

    def update_customer(self):
        if hasattr(self, 'selected_item_id'):
            name = self.name_input.text()
            surname = self.surname_input.text()
            patronymic = self.patronymic_input.text()
            age = self.age_input.text()
            city = self.city_input.text()
            company = self.company_input.text()
            try:
                age = int(age)
                self.db.update_customer(self.selected_item_id, name, surname, patronymic, age, city, company)
                self.populate_table()
            except ValueError:
                QMessageBox.critical(self, 'Error', 'Age must be a number.')
        else:
            QMessageBox.critical(self, 'Error', 'Please select a customer to update.')

    def delete_customer(self):
        if hasattr(self, 'selected_item_id'):
            self.db.delete_customer(self.selected_item_id)
            self.populate_table()
            self.clear_fields()
            delattr(self, 'selected_item_id')
        else:
            QMessageBox.critical(self, 'Error', 'Please select a customer to delete.')

    def clear_fields(self):
        self.name_input.clear()
        self.surname_input.clear()
        self.patronymic_input.clear()
        self.age_input.clear()
        self.city_input.clear()
        self.company_input.clear()

    def search_customers(self):
        search_text = self.search_input.text()
        if search_text:
            self.table.setRowCount(0)
            for row_data in self.db.search_customers(search_text):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, data in enumerate(row_data):
                    self.table.setItem(row_position, col, QTableWidgetItem(str(data)))
        else:
            self.populate_table()


    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                # Write header
                header = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                csv_writer.writerow(header)
                # Write data
                for row in range(self.table.rowCount()):
                    row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                    csv_writer.writerow(row_data)
            QMessageBox.information(self, 'Success', 'Data exported successfully!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database('customers.db')
    main_app = App(db)
    main_app.show()
    sys.exit(app.exec())
