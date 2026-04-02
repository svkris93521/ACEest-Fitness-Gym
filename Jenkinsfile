// ============================================================
// ACEest Fitness & Gym – Jenkinsfile
// Declarative Pipeline for the Jenkins BUILD stage.
//
// Setup:
//   1. Install Jenkins (https://www.jenkins.io/doc/book/installing/)
//   2. Create a new Pipeline project.
//   3. Set "Pipeline script from SCM" → Git → your GitHub repo URL.
//   4. Ensure the Jenkins agent has Python 3.11+ and Docker installed.
// ============================================================

'''pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "==> Checking out source code from GitHub..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "==> Installing Python dependencies..."
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
            }
        }

        stage('Lint') {
            steps {
                echo "==> Running flake8 linter..."
                sh "${PYTHON} -m flake8 app.py tests/ --max-line-length=120 --statistics"
            }
        }

        stage('Test') {
            steps {
                echo "==> Running Pytest suite..."
                sh "${PYTHON} -m pytest tests/ -v --tb=short"
            }
            post {
                always {
                    echo "Tests completed."
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "==> Building Docker image: ${APP_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${APP_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${APP_NAME}:${IMAGE_TAG} ${APP_NAME}:latest"
            }
        }

    }

    post {
        success {
            echo "✅ BUILD SUCCESSFUL – ACEest image ${APP_NAME}:${IMAGE_TAG} is ready."
        }
        failure {
            echo "❌ BUILD FAILED – Review the stage logs above for details."
        }
        always {
            echo "Pipeline finished at ${new Date()}."
        }
    }
}'''

// ============================================================
// ACEest Fitness & Gym – Jenkinsfile (v3.2.4 Optimized)
// ============================================================

pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        // Use BUILD_NUMBER for unique tagging
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        // Set the test DB name to match your app's logic
        DB_NAME     = "test_aceest_jenkins.db"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "==> Checking out source code..."
                checkout scm
            }
        }

        //stage('Install System Dependencies') {
        //    steps {
        //        echo "==> Installing Tkinter and Xvfb for headless GUI testing..."
                // This replaces the sudo apt-get install step from main.yml
        //        sh "sudo apt-get update && sudo apt-get install -y xvfb python3-tk"
        //    }
        //}

        stage('Install Python Dependencies') {
            steps {
                echo "==> Installing requirements (fpdf2, matplotlib, etc.)..."
                sh "${PYTHON} -m pip install --upgrade pip"
                // Ensure numpy<2.0.0 is handled via requirements.txt or manually here
                sh "${PYTHON} -m pip install -r requirements.txt"
            }
        }

        stage('Test (Headless)') {
            steps {
                echo "==> Running Pytest suite with Xvfb virtual display..."
                // 'xvfb-run' is the magic command from our main.yml
                sh "xvfb-run ${PYTHON} -m pytest tests.py -v --tb=short"
            }
            post {
                always {
                    // This archives results so Jenkins can show you the green checkmarks
                    junit testResults: '**/test-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "==> Building Docker image: ${APP_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${APP_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${APP_NAME}:${IMAGE_TAG} ${APP_NAME}:latest"
            }
        }
    }

    post {
        success {
            echo "✅ BUILD SUCCESSFUL – ${APP_NAME}:${IMAGE_TAG} is ready."
        }
        failure {
            echo "❌ BUILD FAILED – Check the Console Output for errors."
        }
    }
}
