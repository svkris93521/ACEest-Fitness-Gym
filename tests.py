import pytest
import sqlite3
import os
import tkinter as tk
from app import app, root

# Use a temporary database for testing
TEST_DB = "test_aceest.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Point the app to a test database and cleanup after tests."""
    # Ensure app uses the test database
    app.conn = sqlite3.connect(TEST_DB)
    app.cur = app.conn.cursor()
    app.init_db()
    yield
    app.conn.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    root.destroy()

def test_db_save_and_calculation(monkeypatch):
    """Test saving a client and verify the calorie calculation in DB."""
    import tkinter.messagebox as mb
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)

    app.name.set("Test Athlete")
    app.weight.set(80.0)
    app.program.set("Muscle Gain (MG)")
    
    app.save_client()
    
    # Verify DB directly (80kg * 35 factor = 2800)
    app.cur.execute("SELECT calories FROM clients WHERE name='Test Athlete'")
    result = app.cur.fetchone()
    assert result[0] == 2800

def test_load_client_ui(monkeypatch):
    """Test that loading a client updates the UI Text widget."""
    import tkinter.messagebox as mb
    monkeypatch.setattr(mb, "showwarning", lambda title, msg: None)

    app.name.set("Test Athlete")
    app.load_client()
    root.update()

    summary = app.summary.get("1.0", "end")
    assert "Test Athlete" in summary
    assert "2800 kcal" in summary

def test_save_progress_entry():
    """Verify progress log adds a row to the progress table."""
    app.name.set("Test Athlete")
    app.adherence.set(90)
    app.save_progress()
    
    app.cur.execute("SELECT adherence FROM progress WHERE client_name='Test Athlete'")
    results = app.cur.fetchall()
    assert len(results) >= 1
    assert results[-1][0] == 90

def test_chart_logic_no_crash(monkeypatch):
    """Ensure the chart function processes data without crashing (Mocking plt.show)."""
    import matplotlib.pyplot as plt
    import tkinter.messagebox as mb
    
    # Mock plt.show() so the test doesn't hang waiting for a window to close
    monkeypatch.setattr(plt, "show", lambda: None)
    monkeypatch.setattr(mb, "showinfo", lambda title, msg: None)

    app.name.set("Test Athlete")
    
    # This should run through the logic of selecting data and creating a plot
    try:
        app.show_progress_chart()
        success = True
    except Exception as e:
        print(f"Chart crashed: {e}")
        success = False
    
    assert success is True
