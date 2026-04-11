pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker compose -f docker-compose.part2.yml down || true'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker compose -f docker-compose.part2.yml up -d --build'
            }
        }
    }
}
