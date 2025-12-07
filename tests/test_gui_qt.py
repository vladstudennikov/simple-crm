import sys
import pytest
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QPoint
from gui_qt import App
from database import Database
import os

@pytest.fixture
def app(qtbot):
    # Use an in-memory database for testing
    db = Database(":memory:")
    test_app = App(db)
    qtbot.addWidget(test_app)
    return test_app

def test_add_customer(app, qtbot):
    app.name_input.setText("test_user")
    app.surname_input.setText("test_surname")
    app.age_input.setText("30")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    assert app.table.rowCount() == 1
    assert app.table.item(0, 1).text() == "test_user"

def test_select_customer(app, qtbot):
    app.name_input.setText("test_user")
    app.surname_input.setText("test_surname")
    app.age_input.setText("30")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    rect = app.table.visualItemRect(app.table.item(0, 0))
    qtbot.mouseClick(app.table.viewport(), Qt.MouseButton.LeftButton, pos=rect.center())
    assert app.name_input.text() == "test_user"

def test_update_customer(app, qtbot):
    app.name_input.setText("test_user")
    app.surname_input.setText("test_surname")
    app.age_input.setText("30")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    rect = app.table.visualItemRect(app.table.item(0, 0))
    qtbot.mouseClick(app.table.viewport(), Qt.MouseButton.LeftButton, pos=rect.center())
    app.name_input.setText("updated_user")
    app.age_input.setText("31")
    qtbot.mouseClick(app.update_btn, Qt.MouseButton.LeftButton)
    assert app.table.item(0, 1).text() == "updated_user"
    assert app.table.item(0, 4).text() == "31"

def test_delete_customer(app, qtbot):
    app.name_input.setText("test_user")
    app.surname_input.setText("test_surname")
    app.age_input.setText("30")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    assert app.table.rowCount() > 0
    rect = app.table.visualItemRect(app.table.item(0, 0))
    qtbot.mouseClick(app.table.viewport(), Qt.MouseButton.LeftButton, pos=rect.center())
    qtbot.mouseClick(app.delete_btn, Qt.MouseButton.LeftButton)
    assert app.table.rowCount() == 0

def test_clear_fields(app, qtbot):
    app.name_input.setText("test_user")
    qtbot.mouseClick(app.clear_btn, Qt.MouseButton.LeftButton)
    assert app.name_input.text() == ""

def test_sorting(app, qtbot):
    app.db.add_customer("B", "B", "B", 20, "B", "B")
    app.db.add_customer("A", "A", "A", 10, "A", "A")
    app.populate_table()
    
    # Sort by name ascending
    app.sort_table(1)
    assert app.table.item(0, 1).text() == "A"
    assert app.table.item(1, 1).text() == "B"
    
    # Sort by name descending
    app.sort_table(1)
    assert app.table.item(0, 1).text() == "B"
    assert app.table.item(1, 1).text() == "A"

def test_search(app, qtbot):
    app.db.add_customer("John", "Doe", "", 30, "", "Google")
    app.db.add_customer("Jane", "Smith", "", 25, "", "Apple")
    app.populate_table()
    
    app.search_input.setText("John")
    qtbot.wait(100) # Wait for the search to trigger
    assert app.table.rowCount() == 1
    assert app.table.item(0, 1).text() == "John"
    
    app.search_input.setText("Apple")
    qtbot.wait(100)
    assert app.table.rowCount() == 1
    assert app.table.item(0, 6).text() == "Apple"

    app.search_input.setText("")
    qtbot.wait(100)
    assert app.table.rowCount() == 2

def test_age_validation(app, qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: None)
    app.name_input.setText("test_user")
    app.age_input.setText("abc")
    qtbot.mouseClick(app.add_btn, Qt.MouseButton.LeftButton)
    assert app.table.rowCount() == 0

def test_export_to_csv(app, qtbot, monkeypatch):
    app.db.add_customer("John", "Doe", "", 30, "", "Google")
    app.populate_table()
    
    mock_file_path = "test.csv"
    monkeypatch.setattr("gui_qt.QFileDialog.getSaveFileName", lambda *args: (mock_file_path, None))
    
    qtbot.mouseClick(app.export_btn, Qt.MouseButton.LeftButton)
    
    assert os.path.exists(mock_file_path)
    with open(mock_file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 2
        assert "John,Doe" in lines[1]
    
    os.remove(mock_file_path)