// =========================================================================================
// ACEest Fitness & Gym – Jenkins CI/CD Pipeline
// Synchronized with main.yml (v3.2.4)
// =========================================================================================

pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        // Unique tag using Jenkins build number, similar to github.sha
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        DB_NAME     = "test_aceest_jenkins.db"
    }

    stages {
        // --- STAGE 1: BUILD & LINT (Replicating main.yml Job 1) ---
        stage('Build & Lint') {
            steps {
                echo "==> Bootstrapping pip and installing dependencies..."
                // Use ensurepip to install pip if it's missing
                sh "${PYTHON} -m ensurepip --default-pip"
        
                // Upgrade pip and install requirements
                sh "${PYTHON} -m pip install --user --upgrade pip"
                sh "${PYTHON} -m pip install --user -r requirements.txt"
        
                '''echo "==> Running Local Tests (Headless)..."
                timeout(time: 3, unit: 'MINUTES') {
                    sh "xvfb-run pytest tests.py"
                }'''
            }
        }

        // --- STAGE 2: DOCKER ASSEMBLY (Replicating main.yml Job 2) ---
        stage('Docker Image Assembly') {
            steps {
                echo "==> Building Docker image: ${APP_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest ."
                
                echo "==> Verifying Docker image..."
                sh "docker images ${APP_NAME}"
            }
        }

        // --- STAGE 3: AUTOMATED TESTING (Containerized) (Replicating main.yml Job 3) ---
        stage('Automated Testing (Container)') {
            steps {
                echo "==> Running Pytest INSIDE the stable Docker container..."
                // --init ensures zombie processes (like Xvfb) are cleaned up correctly
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
        success {
            echo "✅ PIPELINE SUCCESSFUL – ${APP_NAME}:${IMAGE_TAG} is stable."
        }
        failure {
            echo "❌ PIPELINE FAILED – Review Console Output for stage errors."
        }
        always {
            // Clean up the local test database file
            sh "rm -f ${DB_NAME} || true"
        }
    }
}
