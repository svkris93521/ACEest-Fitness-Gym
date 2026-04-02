import pytest
import os
import sqlite3
from app import app, root

# Use a separate database file for testing
TEST_DB = "test_fitness.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Ensure the app uses a test database and cleans up after."""
    # Point the app's connection to the test database
    app.conn = sqlite3.connect(TEST_DB)
    app.cur = app.conn.cursor()
    app.init_db() # Create tables in the test DB
    yield
    app.conn.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    root.destroy()

def test_database_initialization():
    """Verify that tables are created correctly."""
    app.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in app.cur.fetchall()]
    assert "clients" in tables
    assert "progress" in tables

def test_save_and_load_client(monkeypatch):
    """Test the full cycle of saving a client to DB and loading them back."""
    import tkinter.messagebox as mb
    # Mock messageboxes to prevent hanging in GitHub Actions
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)
    monkeypatch.setattr(mb, "showwarning", lambda title, msg: None)

    # 1. Setup Client Data
    app.name.set("Iron Man")
    app.age.set(45)
    app.weight.set(85.0)
    app.program.set("Muscle Gain (MG)")
    
    # 2. Save to DB
    app.save_client()
    
    # 3. Clear fields to prove loading works
    app.age.set(0)
    app.weight.set(0.0)
    
    # 4. Load from DB
    app.load_client()
    root.update()

    # 5. Assertions
    assert app.age.get() == 45
    assert app.weight.get() == 85.0
    summary_content = app.summary.get("1.0", "end")
    assert "Iron Man" in summary_content
    assert "2975 kcal" in summary_content # 85kg * 35 factor

def test_save_progress(monkeypatch):
    """Verify that progress adherence is logged in the progress table."""
    import tkinter.messagebox as mb
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)

    app.name.set("Iron Man")
    app.adherence.set(95)
    
    app.save_progress()
    
    # Check DB directly
    app.cur.execute("SELECT adherence FROM progress WHERE client_name='Iron Man'")
    row = app.cur.fetchone()
    assert row is not None
    assert row[0] == 95

def test_missing_data_error(monkeypatch):
    """Ensure error message triggers when name/program is missing."""
    import tkinter.messagebox as mb
    errors = []
    monkeypatch.setattr(mb, "showerror", lambda title, msg: errors.append(msg))

    app.name.set("") # Missing name
    app.save_client()
    
    assert len(errors) > 0
    assert "Name and Program required" in errors[0]
