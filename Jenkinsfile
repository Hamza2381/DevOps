pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/Hamza2381/DevOps.git'
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
