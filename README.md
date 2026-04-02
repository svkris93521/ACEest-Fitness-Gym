This README.md is designed to showcase your project as a professional, CI/CD-integrated desktop application. It highlights the advanced features of v3.2.4, including the relational database, AI logic, and the stable testing pipeline we built. 
🏋️ ACEest Fitness & Performance Suite (v3.2.4)
ACEest is a professional-grade desktop application built with Python and Tkinter, designed for gym owners and coaches to manage client profiles, track performance metrics, and generate AI-driven workout programs.


🚀 Key Features
Secure Authentication: Role-based access control (Admin/Staff) with a secure login system.
Relational Database: Powered by SQLite, managing 5+ linked tables for Clients, Workouts, Exercises, and Body Metrics.
AI Program Generator: Automatically generates customized training splits based on client goals (Fat Loss, Muscle Gain, etc.).
Visual Analytics: Integrated Matplotlib charts for tracking weekly adherence and progress trends.
Automated Reports: One-click PDF Report Generation using fpdf2 for professional client summaries.
Membership Management: Track membership status and expiry dates with automated status updates.

🛠️ Tech Stack
GUI: Tkinter (Custom Dark Theme)
Database: SQLite3
Visualization: Matplotlib
Reports: fpdf2
Testing: Pytest (100% Headless/CI-Ready)
DevOps: GitHub Actions & Docker

📦 Installation & Setup
Clone the Repository:
bash
git clone https://github.com
cd ACEest-Fitness-Gym
Use code with caution.

Install Dependencies:
Note: We use numpy<2.0.0 to ensure compatibility with Matplotlib.
bash
pip install -r requirements.txt
Use code with caution.

Run the Application:
bash
python3 app.py
Use code with caution.

Default Credentials: admin / admin
🧪 Automated Testing
This project features a stabilized headless test suite designed to run in CI/CD environments (GitHub Actions/Docker) without needing a physical monitor.
To run tests locally:
bash
pytest tests.py
Use code with caution.

What the tests cover:
Database Integrity: Verification of all relational tables and CRUD operations.
Logic Validation: Calorie calculations and AI program mapping.
Mocked UI: Automated testing of messagebox, simpledialog, and filedialog without manual interaction.

🐳 Docker Support
You can run the entire suite in a containerized environment:
bash
docker build -t aceest-fitness-gym .
docker run -it aceest-fitness-gym
Use code with caution.

📈 Roadmap
SQLite Database Integration (v2.x)
Multi-table Relational Schema (v3.0)
Secure RBAC Login System (v3.1)
AI Program Generator & PDF Support (v3.2)
Cloud Database Sync (v4.0)
