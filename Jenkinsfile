pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/opt/jenkins-cicd/Backend'
        VENV_DIR = '/opt/jenkins-cicd/Backend/.venv'
    }

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

        stage('Verify Deployment Environment') {
            steps {
                sh '''
                    test -d "$DEPLOY_DIR"
                    test -x "$VENV_DIR/bin/python"
                    command -v rsync
                    command -v curl
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '"$VENV_DIR/bin/python" -m pip install --disable-pip-version-check -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '"$VENV_DIR/bin/python" -m unittest -v'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    rsync -a \
                        --exclude='.git/' \
                        --exclude='.venv/' \
                        --exclude='__pycache__/' \
                        --exclude='*.py[cod]' \
                        --exclude='.pytest_cache/' \
                        --exclude='.coverage' \
                        --exclude='*.log' \
                        ./ "$DEPLOY_DIR/"
                '''
            }
        }

        stage('Restart Service') {
            steps {
                sh 'sudo -n /usr/bin/systemctl restart flask-backend'
            }
        }

        stage('Verify Health') {
            steps {
                sh '''
                    HTTP_STATUS="$(curl --silent --show-error --max-time 10 \
                        --output /dev/null --write-out '%{http_code}' \
                        http://127.0.0.1:5000/api/health)"

                    if [ "$HTTP_STATUS" != "200" ]; then
                        echo "Health check failed with HTTP status $HTTP_STATUS"
                        exit 1
                    fi

                    echo 'Flask backend health check passed with HTTP status 200.'
                '''
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
