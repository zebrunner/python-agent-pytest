pipeline {
    agent { docker { image 'python:3.7-slim' } }
    stages {
        stage('build') {
            steps {
                sh 'curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -'
            }
        }
        stage('intall-dependencies') {
            steps {
                sh 'poetry install'
            }
        }
    }
}
