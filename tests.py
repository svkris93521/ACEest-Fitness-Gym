import pytest
import tkinter as tk
from app import app, root
import os

@pytest.fixture(scope="session", autouse=True)
def cleanup_gui():
    """Ensure the Tkinter window is destroyed after tests finish."""
    yield
    root.destroy()

def test_initial_ui_elements():
    """Verify new v2 elements are initialized."""
    assert hasattr(app, 'client_table')
    assert hasattr(app, 'canvas')
    assert len(app.clients) == 0

def test_save_client_and_table_update(monkeypatch):
    """Test saving a client updates the internal list and the Treeview."""
    import tkinter.messagebox as mb
    # Mock messagebox to avoid hanging
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)

    app.name_var.set("Test User")
    app.weight_var.set(70.0)
    app.program_var.set("Fat Loss (FL)")
    app.progress_var.set(85)
    
    app.save_client()
    root.update()

    # Check internal data
    assert len(app.clients) == 1
    assert app.clients[0][0] == "Test User"
    
    # Check Table (Treeview)
    children = app.client_table.get_children()
    assert len(children) == 1
    values = app.client_table.item(children[0])['values']
    assert "Test User" in values

def test_calorie_calculation_v2():
    """Verify the calorie logic remains accurate in v2."""
    app.weight_var.set(100.0)
    app.program_var.set("Muscle Gain (MG)")
    app.update_program()
    root.update()
    
    # 100kg * 35 calorie_factor = 3500 kcal
    assert "3500 kcal" in app.calorie_label.cget("text")

def test_csv_export_logic(monkeypatch, tmp_path):
    """Test the CSV export functionality using a temporary file."""
    import tkinter.filedialog as fd
    import tkinter.messagebox as mb

    # 1. CLEAR existing clients from previous tests
    app.clients = [] 
    app.client_table.delete(*app.client_table.get_children())

    # 2. Setup paths
    d = tmp_path / "sub"
    d.mkdir()
    test_file = str(d / "test_export.csv")

    # 3. Mock dialogs
    monkeypatch.setattr(fd, "asksaveasfilename", lambda **kwargs: test_file)
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)

    # 4. Add the specific data we want to find
    app.clients.append(("ExportUser", 25, 75.0, "BG", 90, "Notes"))

    app.export_csv()

    # 5. Verify
    assert os.path.exists(test_file)
    with open(test_file, 'r') as f:
        content = f.read()
        assert "ExportUser" in content
        assert "BG" in content


def test_chart_update_does_not_crash():
    """Ensure the Matplotlib canvas draws without errors."""
    try:
        app.update_chart()
        root.update()
        success = True
    except Exception:
        success = False
    assert success is True
