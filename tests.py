""" import pytest
from app import app  # This imports the 'app' instance from app.py

def test_program_data_exists():

    assert "Fat Loss (FL)" in app.programs
    assert "Muscle Gain (MG)" in app.programs
    assert "Beginner (BG)" in app.programs

def test_initial_label_text():

    assert app.work_label.cget("text") == "Select a profile to view workout"

def test_ui_update_on_selection():

    # Simulate selecting 'Muscle Gain'
    app.prog_var.set("Muscle Gain (MG)")
    
    # Manually trigger the update function
    app.update_display(None)
    
    # Assert the label updated to the correct workout
    assert "Squat 5x5" in app.work_label.cget("text")
    # Assert the color changed to green (as defined in your dict)
    assert app.work_label.cget("fg") == "#2ecc71" """

import pytest
from app import app, root

def test_program_selection():
    # Simulate a user action
    app.prog_var.set("Fat Loss (FL)")
    app.update_display(None)
    
    # Force the UI to refresh so we can check the result
    root.update() 
    
    assert "2,000 kcal" in app.diet_label.cget("text")

