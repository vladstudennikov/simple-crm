import sys
from PyQt6.QtWidgets import QApplication
from database import Database
from gui_qt import App

if __name__ == "__main__":
    db = Database("customers.db")
    app = QApplication(sys.argv)
    main_app = App(db)
    main_app.show()
    sys.exit(app.exec())