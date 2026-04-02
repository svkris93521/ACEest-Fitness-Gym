import pytest
import sqlite3
import os
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys

# 1. MOCK GUI MODULES BEFORE IMPORTING APP
mock_mb = MagicMock()
sys.modules["tkinter.messagebox"] = mock_mb
sys.modules["tkinter.filedialog"] = MagicMock()

from app import ACEestApp

TEST_DB = "test_aceest_v3.db"

@pytest.fixture(scope="session")
def app_instance():
    """Initialize headless app and database for the session."""
    root = tk.Tk()
    root.withdraw() # Hide the window
    
    import app
    app.DB_NAME = TEST_DB
    
    app_instance = ACEestApp(root)
    yield app_instance, root
    
    # Teardown
    app_instance.conn.close()
    root.destroy()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_v3_schema_initialization(app_instance):
    """Verify all 5 new relational tables exist."""
    app, _ = app_instance
    app.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in app.cur.fetchall()]
    
    expected = ["clients", "progress", "workouts", "exercises", "metrics"]
    for table in expected:
        assert table in tables

def test_save_client_v3_logic(app_instance):
    """Test saving with new height/target weight fields and updated program keys."""
    app, _ = app_instance
    
    app.name.set("V3 Athlete")
    app.age.set(25)
    app.height.set(185.0)
    app.weight.set(95.0)
    app.target_weight.set(88.0)
    # FIX: Must match the new string in setup_data exactly
    app.program.set("Muscle Gain (MG) – PPL") 
    
    app.save_client()
    
    app.cur.execute("SELECT height, calories, target_weight FROM clients WHERE name='V3 Athlete'")
    res = app.cur.fetchone()
    assert res[0] == 185.0
    assert res[1] == 3325  # 95kg * 35 factor
    assert res[2] == 88.0

def test_client_list_combobox_sync(app_instance):
    """Verify that the client selection list refreshes after a save."""
    app, _ = app_instance
    app.refresh_client_list()
    
    # Combobox values are stored as a tuple of strings
    assert "V3 Athlete" in app.client_list['values']

def test_metrics_table_insert(app_instance):
    """Directly test metric logging (simulating the Metrics Window logic)."""
    app, _ = app_instance
    
    app.cur.execute("""
        INSERT INTO metrics (client_name, date, weight, waist, bodyfat)
        VALUES (?, ?, ?, ?, ?)
    """, ("V3 Athlete", "2023-10-27", 94.5, 34.2, 18.5))
    app.conn.commit()
    
    app.cur.execute("SELECT waist FROM metrics WHERE client_name='V3 Athlete'")
    assert app.cur.fetchone()[0] == 34.2

@patch("matplotlib.pyplot.show")
def test_history_window_execution(mock_show, app_instance):
    """Ensure the history window logic runs without crashing."""
    app, _ = app_instance
    app.name.set("V3 Athlete")
    
    try:
        # Testing if the method executes its logic properly
        app.open_workout_history_window()
        success = True
    except Exception as e:
        print(f"Window logic failed: {e}")
        success = False
    assert success is True
