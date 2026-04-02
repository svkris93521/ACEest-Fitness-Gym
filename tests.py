import pytest
from app import app, root

@pytest.fixture(scope="session", autouse=True)
def cleanup_gui():
    """Ensure the Tkinter window is destroyed after tests finish."""
    yield
    root.destroy()

def test_initial_state():
    """Verify that the app starts with empty fields."""
    assert app.name_var.get() == ""
    assert app.weight_var.get() == 0.0
    assert "Estimated Calories: --" in app.calorie_label.cget("text")

def test_program_selection_logic():
    """Test if selecting a program updates the workout and calorie calculations."""
    # 1. Set a weight
    app.weight_var.set(80.0)
    
    # 2. Select 'Muscle Gain'
    app.program_var.set("Muscle Gain (MG)")
    
    # 3. Manually trigger the update
    app.update_program()
    root.update()

    # 4. Check workout text (extract from tk.Text widget)
    workout_content = app.workout_text.get("1.0", "end-1c")
    assert "Squat 5x5" in workout_content
    
    # 5. Check calorie calculation (80kg * 35 calorie_factor = 2800)
    assert "2800 kcal" in app.calorie_label.cget("text")

def test_reset_functionality():
    """Verify the reset button clears all fields."""
    # Fill data
    app.name_var.set("John Doe")
    app.program_var.set("Fat Loss (FL)")
    
    # Reset
    app.reset()
    root.update()
    
    assert app.name_var.get() == ""
    assert app.program_var.get() == ""
    assert "Estimated Calories: --" in app.calorie_label.cget("text")

def test_save_validation(monkeypatch):
    """Test that saving fails if name is missing (mocking the messagebox)."""
    import tkinter.messagebox as mb
    
    # Mock the showwarning to prevent a popup hanging the test
    monkeypatch.setattr(mb, "showwarning", lambda title, msg: None)
    
    app.name_var.set("") # Empty name
    app.program_var.set("Beginner (BG)")
    
    # Should trigger validation logic
    app.save_client() 
    # (The test passes if it runs without error/hang)
