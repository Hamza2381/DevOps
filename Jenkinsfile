pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker compose -f docker-compose.part2.yml down || true'
            }
        }

        stage('Run Container (Part 2)') {
            steps {
                sh 'docker compose -f docker-compose.part2.yml up -d'
            }
        }
    }
}

