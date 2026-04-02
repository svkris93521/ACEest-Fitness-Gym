import pytest
import sqlite3
import os
import tkinter as tk
from unittest.mock import MagicMock
import sys

# 1. MOCK GUI MODULES
mock_mb = MagicMock()
sys.modules["tkinter.messagebox"] = mock_mb
sys.modules["tkinter.filedialog"] = MagicMock()

from app import ACEestApp

TEST_DB = "test_v3_aceest.db"

@pytest.fixture(scope="session")
def app_instance():
    """Initialize headless app and database for the session."""
    root = tk.Tk()
    root.withdraw()
    
    import app
    app.DB_NAME = TEST_DB
    
    app_instance = ACEestApp(root)
    yield app_instance, root
    
    # Teardown
    app_instance.conn.close()
    root.destroy()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_save_client_logic_v3(app_instance):
    """Test saving a client with the new V3 program names."""
    app, _ = app_instance
    
    app.name.set("Superman")
    app.weight.set(90.0)
    # UPDATED: Must match exactly one of the new keys in app.py
    app.program.set("Muscle Gain (MG) – PPL") 
    
    # Trigger the save logic
    app.save_client()
    
    # Verify DB: 90kg * 35 factor = 3150 calories
    app.cur.execute("SELECT calories FROM clients WHERE name='Superman'")
    result = app.cur.fetchone()
    assert result[0] == 3150

def test_load_client_to_ui_v3(app_instance):
    """Test loading a saved client updates the UI summary."""
    app, root = app_instance
    
    # Ensure client exists in DB first
    app.name.set("Superman")
    app.load_client()
    root.update()
    
    # Check the summary text area
    summary = app.summary.get("1.0", "end")
    assert "Superman" in summary
    assert "3150 kcal" in summary

def test_client_list_refresh_v3(app_instance):
    """Verify the new selection combobox contains the saved client."""
    app, _ = app_instance
    app.refresh_client_list()
    assert "Superman" in app.client_list['values']
