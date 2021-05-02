pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            args '-u root'
        }
    }
    environment {
        REPORTING_SERVER_HOSTNAME = 'https://pytesttest.qaprosoft.farm'
        REPORTING_SERVER_ACCESS_TOKEN = 'eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJSMlbSUSpILC4uzy9KAXK9A0tyI4OjKtPTgtOywivzsvPcDAu9jUoy83IsszLKzICqS1LzEvNKgGoLKktSi0tAGCiaWVwMFMpMzAWyUysKlKyMzc3MTUzMjczNawE7rUXhbAAAAA.c3cswK2ODHqA6DLfWulmf08QHTHivY5tts9l1KAajQ_K5o6rO0QR0Hu-XkfCuXLISd7qKh1dDd4gH1cekVcy1A'
        REPORTING_PROJECT_KEY = 'PYT'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'develop', url: 'https://github.com/zebrunner/python-agent-pytest.git'
            }
        }
        stage('Intall requirements') {
            steps {
                sh 'poetry install'
            }
        }
        stage('Testing') {
            steps {
                sh 'poetry run pytest'
            }
        }
    }
}
