// =========================================================================================
// ACEest Fitness & Gym – Optimized Jenkins CI/CD (Headless Stable)
// =========================================================================================

pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        DB_NAME     = "test_aceest_jenkins.db"
        // Force Python to not write .pyc files and buffer output for cleaner logs
        PYTHONDONTWRITEBYTECODE = 1
        PYTHONUNBUFFERED = 1
    }

    stages {
        // --- STAGE 1: LOCAL VALIDATION ---
        stage('Build & Lint') {
            steps {
                echo "==> Bootstrapping pip and installing dependencies..."
                // Use ensurepip to install pip if it's missing
                sh "${PYTHON} -m ensurepip --default-pip"
        
                // Upgrade pip and install requirements
                sh "${PYTHON} -m pip install --user --upgrade pip"
                sh "${PYTHON} -m pip install --user -r requirements.txt"
        
                echo "==> Running Local Tests (Headless)..."
                timeout(time: 3, unit: 'MINUTES') {
                    //sh "${PYTHON} -m pytest tests.py -v"
                    sh "${PYTHON} -m py_compile app.py tests.py"
                }
            }
        }

        // --- STAGE 2: DOCKER BUILD ---
        stage('Docker Image Assembly') {
            steps {
                echo "==> Building Docker image: ${APP_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest ."
                
                echo "==> Verifying Docker image..."
                sh "docker images ${APP_NAME}"
            }
        }

        // --- STAGE 3: HEADLESS AUTOMATED TESTING ---
        stage('Automated Testing (Container)') {
            steps {
                echo "==> Running Pytest INSIDE the container using Xvfb..."
                timeout(time: 5, unit: 'MINUTES') {
                    sh """
                        docker run --rm --init \
                        ${APP_NAME}:latest \
                        bash -c "apt-get update && apt-get install -y xvfb && xvfb-run python3 -m pytest tests.py"
                    """
                    sh "docker run -d --name ${APP_NAME} -p 9000:8080 ${APP_NAME}:latest"
                }
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE SUCCESSFUL – ${APP_NAME}:${IMAGE_TAG} is ready for deployment."
        }
        failure {
            echo "❌ PIPELINE FAILED – Check the Xvfb or Tkinter logs in Console Output."
        }
        always {
            sh "rm -f ${DB_NAME} || true"
        }
    }
}