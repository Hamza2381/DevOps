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
                sh 'docker stop part2_app || true'
                sh 'docker rm part2_app || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                  --name part2_app \
                  -p 5001:4000 \
                  -v $(pwd):/app \
                  -w /app \
                  node:18 \
                  sh -c "npm install && npm start"
                '''
            }
        }
    }
}
