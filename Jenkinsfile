pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.part2.yml'
        APP_CONTAINER = 'webapp_part2'
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo '📥 Cloning latest code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/Hamza2381/DevOps.git'
            }
        }

        stage('Stop Old Containers') {
            steps {
                echo '🛑 Stopping existing Part II containers...'
                sh 'docker-compose -f ${COMPOSE_FILE} down --remove-orphans || true'
            }
        }

        stage('Build & Start Application') {
            steps {
                echo '🚀 Starting containerized app with code volume...'
                sh 'docker-compose -f ${COMPOSE_FILE} up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '🔍 Verifying containers are running...'
                sh 'docker ps'
                sh 'sleep 5'
                sh "docker logs ${APP_CONTAINER} --tail=30 || true"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! App running on port 8081.'
        }
        failure {
            echo '❌ Pipeline failed. Dumping logs...'
            sh "docker-compose -f ${COMPOSE_FILE} logs --tail=50 || true"
        }
    }
}
