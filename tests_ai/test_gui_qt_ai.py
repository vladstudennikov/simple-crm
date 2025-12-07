
import sys
import pytest
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from gui_qt import App
from database import Database

@pytest.fixture
def app(qtbot):
    db = Database(":memory:")
    test_app = App(db)
    qtbot.addWidget(test_app)
    return test_app

def test_add_customer_with_all_fields(app, qtbot):
    app.name_input.setText("test_name")
    app.surname_input.setText("test_surname")
    app.patronymic_input.setText("test_patronymic")
    app.age_input.setText("25")
    app.city_input.setText("test_city")
    app.company_input.setText("test_company")
    
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    
    assert app.table.rowCount() == 1
    assert app.table.item(0, 1).text() == "test_name"
    assert app.table.item(0, 2).text() == "test_surname"
    assert app.table.item(0, 3).text() == "test_patronymic"
    assert app.table.item(0, 4).text() == "25"
    assert app.table.item(0, 5).text() == "test_city"
    assert app.table.item(0, 6).text() == "test_company"

def test_add_customer_empty_name_validation(app, qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: None)
    app.name_input.setText("")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    assert app.table.rowCount() == 0

def test_update_customer_no_selection_validation(app, qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: None)
    qtbot.mouseClick(app.update_btn, Qt.MouseButton.LeftButton)
    # No assert needed, we are just checking that it doesn't crash and shows a message box

def test_update_customer_age_validation(app, qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: None)
    app.name_input.setText("test_user")
    app.age_input.setText("30")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    
    rect = app.table.visualItemRect(app.table.item(0, 0))
    qtbot.mouseClick(app.table.viewport(), Qt.MouseButton.LeftButton, pos=rect.center())
    
    app.age_input.setText("abc")
    qtbot.mouseClick(app.update_btn, Qt.MouseButton.LeftButton)
    assert app.table.item(0, 4).text() == "30" # Age should not have been updated

def test_delete_customer_no_selection_validation(app, qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: None)
    qtbot.mouseClick(app.delete_btn, Qt.MouseButton.LeftButton)
    # No assert needed, we are just checking that it doesn't crash and shows a message box

def test_initial_ui_state(app, qtbot):
    assert app.windowTitle() == 'Modern CRM'
    assert app.table.columnCount() == 7
    assert app.table.horizontalHeaderItem(0).text() == 'ID'
    assert app.table.horizontalHeaderItem(1).text() == 'Name'
    assert app.table.horizontalHeaderItem(2).text() == 'Surname'
    assert app.table.horizontalHeaderItem(3).text() == 'Patronymic'
    assert app.table.horizontalHeaderItem(4).text() == 'Age'
    assert app.table.horizontalHeaderItem(5).text() == 'City'
    assert app.table.horizontalHeaderItem(6).text() == 'Company'
