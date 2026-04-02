# ACEest Fitness & Gym

ACEest Fitness & Gym is a Python-based application designed for gym management. This repository includes a complete CI/CD pipeline configuration using Jenkins and Docker.

## Project Structure

- `app.py`: Main application logic.
- `requirements.txt`: Python dependencies.
- `tests/`: Directory containing the Pytest suite.
- `Jenkinsfile`: Declarative pipeline for automated Build, Lint, Test, and Dockerization.
- `Dockerfile`: Instructions for containerizing the application.

## Prerequisites

Before running the pipeline or the application, ensure you have the following installed:
- **Python 3.11+**
- **Docker**
- **Jenkins** (with Pipeline and Docker plugins)

## CI/CD Pipeline Stages

The included `Jenkinsfile` automates the following workflow:

1.  **Checkout**: Pulls the latest source code from the GitHub repository.
2.  **Install Dependencies**: Upgrades `pip` and installs requirements from `requirements.txt`.
3.  **Lint**: Uses `flake8` to check for PEP8 compliance and code quality (max line length 120).
4.  **Test**: Executes the test suite using `pytest` with verbose output.
5.  **Docker Build**: Builds a new Docker image tagged with the Jenkins build number and updates the `latest` tag.

## Local Setup

To run the application locally:

```bash
# Clone the repository
git clone https://github.com/your-username/aceest-fitness.git
cd aceest-fitness

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Run tests
pytest tests/
```

## Docker Usage

To build and run the container manually:

```bash
docker build -t aceest-fitness:latest .
docker run -p 8080:8080 aceest-fitness:latest
```

---
*Developed as part of the DevOps course - BITS Pilani.*