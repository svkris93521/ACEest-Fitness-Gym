// =========================================================================================
// ACEest Fitness & Gym – Jenkins CI/CD Pipeline
// Synchronized with main.yml (v3.2.4)
// =========================================================================================

pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        // Unique tag using Jenkins build number
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        DB_NAME     = "test_aceest_jenkins.db"
    }

    stages {
        // --- STAGE 1: BUILD & LINT (Local Runner) ---
        stage('Build & Lint') {
            steps {
                echo "==> Installing System Dependencies (Tkinter/Xvfb)..."
                sh "sudo apt-get update && sudo apt-get install -y xvfb python3-tk"
                
                echo "==> Installing Python Dependencies..."
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
                
                echo "==> Running Local Tests (Headless)..."
                // timeout(time: 3, unit: 'MINUTES') matches 'timeout-minutes: 3'
                timeout(time: 3, unit: 'MINUTES') {
                    sh "xvfb-run ${PYTHON} -m pytest tests.py -v"
                }
            }
        }

        // --- STAGE 2: DOCKER ASSEMBLY ---
        stage('Docker Image Assembly') {
            steps {
                echo "==> Building Docker image: ${APP_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest ."
                
                echo "==> Verifying Docker image..."
                sh "docker images ${APP_NAME}"
            }
        }

        // --- STAGE 3: AUTOMATED TESTING (Containerized) ---
        stage('Automated Testing (Container)') {
            steps {
                echo "==> Running Pytest INSIDE the Docker container..."
                // Using --init as per your main.yml to handle signal forwarding
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
            echo "✅ CI/CD PIPELINE COMPLETE – ${APP_NAME}:${IMAGE_TAG} is stable."
        }
        failure {
            echo "❌ PIPELINE FAILED – Check stage logs for details."
            // Archive results if they exist (JUnit plugin required in Jenkins)
            archiveArtifacts artifacts: '**/results.xml', allowEmptyArchive: true
        }
        always {
            echo "Pipeline finished at ${new Date()}"
        }
    }
}
