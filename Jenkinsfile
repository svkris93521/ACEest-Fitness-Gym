pipeline {
    agent any

    environment {
        APP_NAME    = 'aceest-fitness-gym'
        PYTHON      = 'python3'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        DB_NAME     = "test_aceest_jenkins.db"
    }

    stages {
        //stage('Install System Dependencies') {
        //    steps {
        //        echo "==> Using credentials to run sudo commands..."
         //       // Intercept the 'sudo' prompt by piping the password from credentials
         //       withCredentials([string(credentialsId: 'SUDO_PASS', variable: 'PASS')]) {
         //           sh "echo '${PASS}' | sudo -S apt-get update"
         //           sh "echo '${PASS}' | sudo -S apt-get install -y xvfb python3-tk python3-pip"
         //       }
         //   }
        //}

        stage('Install System Dependencies') {
            steps {
                echo "==> Using credentials to run sudo commands..."
                withCredentials([string(credentialsId: 'SUDO_PASS', variable: 'PASS')]) {
                    // Use double quotes but escape the $ with \
                    sh "echo \"\$PASS\" | sudo -S apt-get update"
                    sh "echo \"\$PASS\" | sudo -S apt-get install -y xvfb python3-tk python3-pip"
                }
            }
        }


        stage('Install Python Dependencies') {
            steps {
                echo "==> Upgrading pip and installing requirements..."
                sh "${PYTHON} -m ensurepip --default-pip || true"
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
            }
        }

        stage('Test (Local Headless)') {
            steps {
                timeout(time: 3, unit: 'MINUTES') {
                    sh "xvfb-run ${PYTHON} -m pytest tests.py -v"
                }
            }
        }

        stage('Docker Assembly & Test') {
            steps {
                echo "==> Building and verifying container..."
                sh "docker build -t ${APP_NAME}:latest ."
                timeout(time: 3, unit: 'MINUTES') {
                    sh "docker run --rm --init ${APP_NAME}:latest xvfb-run python3 -m pytest tests.py"
                }
            }
        }
    }

    post {
        success { echo "✅ BUILD SUCCESSFUL" }
        failure { echo "❌ BUILD FAILED - Check credentials or sudoers config" }
        always { sh "rm -f ${DB_NAME} || true" }
    }
}
