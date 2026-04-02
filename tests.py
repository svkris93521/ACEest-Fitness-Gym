import pytest
import sqlite3
import os
import tkinter as tk
from unittest.mock import MagicMock, patch

# 1. MOCK GUI MODULES BEFORE IMPORTING APP
# This prevents any real windows or popups from ever appearing
mock_mb = MagicMock()
import sys
sys.modules["tkinter.messagebox"] = mock_mb
sys.modules["tkinter.filedialog"] = MagicMock()

# Now import the App class
from app import ACEestApp

TEST_DB = "test_aceest.db"

@pytest.fixture(scope="session")
def app_instance():
    """Create a headless app instance for the test session."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Force the app to use a test database
    import app
    app.DB_NAME = TEST_DB
    
    app_instance = ACEestApp(root)
    yield app_instance, root
    
    # Cleanup after all tests
    app_instance.conn.close()
    root.destroy()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_db_initialization(app_instance):
    """Verify tables are created in the test database."""
    app, _ = app_instance
    app.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in app.cur.fetchall()]
    assert "clients" in tables
    assert "progress" in tables

def test_save_client_logic(app_instance):
    """Test saving a client and the calorie calculation logic."""
    app, _ = app_instance
    
    app.name.set("Superman")
    app.weight.set(90.0)
    app.program.set("Muscle Gain (MG)")
    
    # Trigger the save logic
    app.save_client()
    
    # Verify DB: 90kg * 35 factor = 3150 calories
    app.cur.execute("SELECT calories FROM clients WHERE name='Superman'")
    result = app.cur.fetchone()
    assert result[0] == 3150

def test_load_client_to_ui(app_instance):
    """Test loading a saved client updates the UI summary."""
    app, root = app_instance
    
    app.name.set("Superman")
    app.load_client()
    root.update()
    
    summary = app.summary.get("1.0", "end")
    assert "Superman" in summary
    assert "3150 kcal" in summary

def test_progress_logging(app_instance):
    """Verify that weekly progress is added to the database."""
    app, _ = app_instance
    
    app.name.set("Superman")
    app.adherence.set(100)
    app.save_progress()
    
    app.cur.execute("SELECT adherence FROM progress WHERE client_name='Superman'")
    row = app.cur.fetchone()
    assert row[0] == 100

@patch("matplotlib.pyplot.show")
def test_chart_logic_headless(mock_show, app_instance):
    """Test chart generation logic without opening a Matplotlib window."""
    app, _ = app_instance
    
    app.name.set("Superman")
    
    # If Superman has progress data, this should build the plot and call mock_show
    try:
        app.show_progress_chart()
        success = True
    except Exception as e:
        print(f"Chart logic failed: {e}")
        success = False
        
    assert success is True
    # Verify that the code tried to 'show' a chart
    assert mock_show.called
