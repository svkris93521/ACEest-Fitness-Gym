pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        DB_NAME     = "test_aceest_jenkins.db"
    }

    stages {
        stage('Install System Dependencies') {
            steps {
                echo "==> Installing Tkinter, Xvfb, and PIP..."
                // Add python3-pip to this list
                sh "sudo apt-get update && sudo apt-get install -y xvfb python3-tk python3-pip"
            }
        }
        // --- STAGE 1: INSTALL & LINT (No Sudo) ---
        stage('Install & Lint') {
            steps {
                echo "==> Installing Python Dependencies..."
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
                
                // Note: We skip local 'xvfb-run' here because it requires sudo to install
                // We will rely on the Containerized tests for GUI validation.
            }
        }

        // --- STAGE 2: DOCKER ASSEMBLY ---
        stage('Docker Image Assembly') {
            steps {
                echo "==> Building Docker image..."
                // Ensure your Dockerfile has: RUN apt-get install -y xvfb python3-tk
                sh "docker build -t ${APP_NAME}:latest ."
            }
        }

        // --- STAGE 3: AUTOMATED TESTING (The Real Test) ---
        stage('Automated Testing (Container)') {
            steps {
                echo "==> Running Pytest INSIDE the Docker container..."
                timeout(time: 3, unit: 'MINUTES') {
                    sh """
                        docker run --rm --init \
                        ${APP_NAME}:latest \
                        xvfb-run python3 -m pytest tests.py
                    """
                }
            }
        }
    }

    post {
        success { echo "✅ BUILD SUCCESSFUL" }
        failure { echo "❌ BUILD FAILED" }
    }
}
