pipeline {
    agent any

    stages {

        stage('Stop Old Container') {
            steps {
                sh 'docker-compose -f docker-compose.part2.yml down || true'
            }
        }

        stage('Run Container (Part 2)') {
            steps {
                sh 'docker-compose -f docker-compose.part2.yml up -d --build'
            }
        }
    }
}
