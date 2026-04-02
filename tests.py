import pytest
from app import app  # This imports the 'app' instance from app.py

def test_program_data_exists():
    """Check if the workout/diet data is loaded correctly."""
    assert "Fat Loss (FL)" in app.programs
    assert "Muscle Gain (MG)" in app.programs
    assert "Beginner (BG)" in app.programs

def test_initial_label_text():
    """Verify the default text before a user selects a program."""
    assert app.work_label.cget("text") == "Select a profile to view workout"

def test_ui_update_on_selection():
    """Simulate a user selecting a program and check if the UI updates."""
    # Simulate selecting 'Muscle Gain'
    app.prog_var.set("Muscle Gain (MG)")
    
    # Manually trigger the update function
    app.update_display(None)
    
    # Assert the label updated to the correct workout
    assert "Squat 5x5" in app.work_label.cget("text")
    # Assert the color changed to green (as defined in your dict)
    assert app.work_label.cget("fg") == "#2ecc71"
