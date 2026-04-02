import pytest
import sqlite3
import os
import tkinter as tk
from app import ACEestApp

# Use a temporary database for testing
TEST_DB = "test_aceest.db"

@pytest.fixture(scope="module")
def app_context():
    """Initializes the Tkinter root and the App for the test session."""
    root = tk.Tk()
    # Override the DB name before initializing the app
    import app
    app.DB_NAME = TEST_DB 
    
    app_instance = ACEestApp(root)
    yield app_instance, root
    
    # Cleanup after tests
    app_instance.conn.close()
    root.destroy()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_database_creation(app_context):
    """Verify that tables are created in the test database."""
    app_instance, _ = app_context
    app_instance.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in app_instance.cur.fetchall()]
    assert "clients" in tables
    assert "progress" in tables

def test_save_and_load_client(app_context, monkeypatch):
    """Test saving a client to SQLite and loading them back into the UI."""
    app_instance, root = app_context
    import tkinter.messagebox as mb
    
    # Mock messageboxes to prevent tests from hanging
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)
    monkeypatch.setattr(mb, "showerror", lambda title, msg: None)

    # 1. Setup Data
    app_instance.name.set("Test Athlete")
    app_instance.age.set(30)
    app_instance.weight.set(70.0)
    app_instance.program.set("Fat Loss (FL)")
    
    # 2. Save
    app_instance.save_client()
    
    # 3. Clear fields
    app_instance.name.set("Test Athlete") # Keep name to load
    app_instance.weight.set(0.0)
    
    # 4. Load
    app_instance.load_client()
    root.update()

    # 5. Assertions
    assert app_instance.weight.get() == 70.0
    summary = app_instance.summary.get("1.0", "end")
    assert "Test Athlete" in summary
    assert "1540 kcal" in summary # 70kg * 22 factor

def test_save_progress_log(app_context, monkeypatch):
    """Verify that progress adherence is correctly logged in the database."""
    app_instance, _ = app_context
    import tkinter.messagebox as mb
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)

    app_instance.name.set("Test Athlete")
    app_instance.adherence.set(95)
    
    app_instance.save_progress()
    
    # Query database directly to verify record
    app_instance.cur.execute("SELECT adherence FROM progress WHERE client_name='Test Athlete'")
    result = app_instance.cur.fetchone()
    assert result is not None
    assert result[0] == 95

def test_error_on_missing_fields(app_context, monkeypatch):
    """Verify that error message triggers if required fields are empty."""
    app_instance, _ = app_context
    import tkinter.messagebox as mb
    
    errors = []
    monkeypatch.setattr(mb, "showerror", lambda title, msg: errors.append(msg))

    app_instance.name.set("") # Empty Name
    app_instance.save_client()
    
    assert "Name and Program required" in errors
