pipeline {
    agent any

    stages {

        stage('Stop Old Container') {
            steps {
                sh '''
                docker rm -f part2_app || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                  --name part2_app \
                  -p 5001:3000 \
                  -v $WORKSPACE:/app \
                  -w /app \
                  node:18 \
                  sh -c "npm install && npm start"
                '''
            }
        }
    }
}
