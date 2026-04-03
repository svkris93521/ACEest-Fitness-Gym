pipeline {
    agent any
    stages {
        stage('Docker Build') {
            steps {
                // The Dockerfile handles all the heavy lifting
                sh "docker build -t aceest-app:latest ."
            }
        }
        stage('Automated Test') {
            steps {
                // Run EVERYTHING inside the container
                // Containers are isolated, so they don't need host sudo
                sh "docker run --rm aceest-app:latest xvfb-run pytest tests.py"
            }
        }
    }
}
