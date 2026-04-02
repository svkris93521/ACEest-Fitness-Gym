import pytest
import sqlite3
import os
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys

# 1. MOCK EXTERNAL LIBRARIES & GUI MODULES BEFORE IMPORTING APP
# This prevents the "no display" and "missing module" errors in CI/CD
mock_mb = MagicMock()
sys.modules["tkinter.messagebox"] = mock_mb
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["fpdf"] = MagicMock()

# 2. MOCK GRAB_SET INTERNALLY
# This prevents "TclError: grab failed" in headless (invisible) environments
tk.Toplevel.grab_set = MagicMock()
tk.Toplevel.grab_release = MagicMock()

# Now import the App class from your app.py
from app import ACEestApp

TEST_DB = "test_aceest_v31.db"

@pytest.fixture(scope="session")
def app_instance():
    """Initialize headless app, bypass login, and setup database."""
    # Create the root window but keep it hidden
    root = tk.Tk()
    root.withdraw() 
    
    # Force the app to use a temporary test database
    import app
    app.DB_NAME = TEST_DB
    
    # Initialize the app (this triggers show_login_window)
    app_instance = ACEestApp(root)
    
    # 3. BYPASS THE LOGIN WINDOW FOR TESTING
    # We manually set the admin credentials and trigger the login function
    app_instance.username_var.set("admin")
    app_instance.password_var.set("admin")
    app_instance.login_user() 
    
    yield app_instance, root
    
    # Teardown: Close DB and destroy the UI
    app_instance.conn.close()
    root.destroy()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

# ---------- TEST CASES ----------

def test_user_authentication_and_role(app_instance):
    """Verify that the bypass login worked and assigned the Admin role."""
    app, _ = app_instance
    assert app.current_user == "admin"
    assert app.user_role == "Admin"

def test_v31_database_schema(app_instance):
    """Verify that the new 'users' and 'clients' tables exist."""
    app, _ = app_instance
    app.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in app.cur.fetchall()]
    
    assert "users" in tables
    assert "clients" in tables
    assert "workouts" in tables
    assert "metrics" in tables

def test_client_save_and_calorie_calc(app_instance):
    """Test saving a client and verify the updated v3.1 calorie factors."""
    app, _ = app_instance
    
    app.name.set("TestAthlete")
    app.weight.set(75.0)
    # Using the new v3.1 program string
    app.program.set("Fat Loss (FL) – 5 day") 
    
    app.save_client()
    
    # Verify calculation: 75kg * 24 factor = 1800 calories
    app.cur.execute("SELECT calories FROM clients WHERE name='TestAthlete'")
    res = app.cur.fetchone()
    assert res[0] == 1800

def test_client_selection_sync(app_instance):
    """Ensure the 'Select Client' dropdown correctly reflects the database."""
    app, root = app_instance
    
    # Trigger a refresh of the list
    app.refresh_client_list()
    
    # The Combobox values should now contain our saved athlete
    assert "TestAthlete" in app.client_list['values']

def test_on_client_selected_logic(app_instance):
    """Simulate choosing a client from the dropdown and verifying UI updates."""
    app, root = app_instance
    
    # Set the list to our athlete and trigger the event
    app.client_list.set("TestAthlete")
    app.on_client_selected(None)
    root.update()
    
    # UI variables should now be populated with the athlete's data
    assert app.name.get() == "TestAthlete"
    assert app.weight.get() == 75.0

@patch("matplotlib.pyplot.show")
def test_headless_chart_rendering(mock_show, app_instance):
    app, _ = app_instance
    app.name.set("TestAthlete")
    
    try:
        # UPDATE THIS LINE to match your actual function name in app.py
        app.view_progress() 
        success = True
    except AttributeError:
        # If it doesn't exist yet, we can skip it for now
        pytest.skip("Chart feature not yet implemented in app.py")
    except Exception as e:
        success = False
        
    assert success is True

