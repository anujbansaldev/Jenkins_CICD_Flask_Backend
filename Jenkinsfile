pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '.venv/bin/python -m unittest -v'
            }
        }
    }

    post {
        success {
            echo 'Flask backend validation passed.'
        }
        failure {
            echo 'Flask backend pipeline failed. Review the console log.'
        }
    }
}
