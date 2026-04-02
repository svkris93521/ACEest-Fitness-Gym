import pytest
import sqlite3
import os
import tkinter as tk
from tkinter import ttk
from unittest.mock import MagicMock, patch
import sys

# 1. MOCK EXTERNAL LIBRARIES & GUI DIALOGS BEFORE IMPORT
# This prevents "no display" and "missing module" errors in CI/CD
mock_mb = MagicMock()
sys.modules["tkinter.messagebox"] = mock_mb
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["fpdf2"] = MagicMock()

# 2. PREVENT HEADLESS TCL ERRORS BY MOCKING BLOCKING GUI METHODS
tk.Toplevel.grab_set = MagicMock()
tk.Toplevel.grab_release = MagicMock()

# Mock Treeview.heading globally to prevent Tcl synchronization crashes
original_heading = ttk.Treeview.heading
ttk.Treeview.heading = MagicMock()

# Import the App and the DB init function
from app import ACEestApp, init_db
import app as app_module

TEST_DB = "test_aceest_v32_final.db"

@pytest.fixture(scope="session")
def app_instance():
    """Initialize headless app, run DB init, and bypass login."""
    app_module.DB_NAME = TEST_DB
    init_db()

    root = tk.Tk()
    root.withdraw() # Hide the main window
    
    app_instance = ACEestApp(root)
    
    # LOGIN BYPASS: Fill vars and call the login method
    app_instance.username_var.set("admin")
    app_instance.password_var.set("admin")
    app_instance.login() 
    
    yield app_instance, root
    
    # Teardown
    app_instance.conn.close()
    root.destroy()
    # Restore original heading after tests
    ttk.Treeview.heading = original_heading
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

# ---------- TEST CASES ----------

def test_admin_login_and_dashboard_load(app_instance):
    """Verify that the login flow correctly initializes the dashboard."""
    app, _ = app_instance
    assert app.current_user == "admin"
    assert app.current_role == "Admin"

def test_database_schema_v32(app_instance):
    """Verify all relational tables are correctly initialized in the test DB."""
    app, _ = app_instance
    app.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in app.cur.fetchall()]
    
    expected_tables = ["users", "clients", "workouts", "exercises", "metrics"]
    for table in expected_tables:
        assert table in tables

def test_add_client_logic(app_instance, monkeypatch):
    """Test the Add Client logic using mocked simpledialog."""
    app, _ = app_instance
    # We must mock 'app.simpledialog' because that's where the app is looking
    import app as app_module
    
    # Mock the popup to return "Iron Man"
    monkeypatch.setattr(app_module.simpledialog, "askstring", lambda title, prompt: "Iron Man")
    
    app.add_save_client()
    
    # Verify the client was added to the database
    app.cur.execute("SELECT membership_status FROM clients WHERE name='Iron Man'")
    res = app.cur.fetchone()
    assert res is not None
    assert res[0] == "Active"
    assert "Iron Man" in app.client_list['values']

def test_ai_program_generation(app_instance):
    """Verify the AI generator assigns a program string to the current client."""
    app, _ = app_instance
    
    # Ensure "Iron Man" exists in DB to prevent NoneType errors in refresh_summary
    app.cur.execute("INSERT OR IGNORE INTO clients (name, membership_status) VALUES (?,?)", 
                   ("Iron Man", "Active"))
    app.conn.commit()
    
    app.current_client = "Iron Man"
    app.generate_program()
    
    # Verify a program was updated in the DB
    app.cur.execute("SELECT program FROM clients WHERE name='Iron Man'")
    program = app.cur.fetchone()
    assert program is not None
    assert program[0] is not None

@patch("matplotlib.pyplot.show")
def test_charts_no_crash(mock_show, app_instance):
    """Ensure charting logic runs without crashing the Tcl interpreter."""
    app, _ = app_instance
    app.current_client = "Iron Man"
    
    try:
        app.plot_charts()
        success = True
    except Exception as e:
        print(f"Chart error: {e}")
        success = False
        
    assert success is True
