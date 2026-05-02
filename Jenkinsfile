pipeline {
    agent any

    environment {
        APP_IMAGE   = "job-portal-app"
        TEST_IMAGE  = "job-portal-tests"
        APP_URL     = "http://localhost:3000"
        RESULTS_DIR = "${WORKSPACE}/test-results"
    }

    stages {

        stage('Checkout') {
            steps {
                echo ">>> Pulling code from GitHub..."
                git branch: 'main',
                    url: 'https://github.com/Hamza2381/DevOps.git'
            }
        }

        stage('Build App Image') {
            steps {
                echo ">>> Building Job Portal Docker image..."
                sh "docker build -t ${APP_IMAGE}:latest ."
            }
        }

        stage('Start Application') {
            steps {
                echo ">>> Starting app container on port 3000..."
                sh "docker rm -f jobportal-running 2>/dev/null || true"
                sh """
                    docker run -d \
                        --name jobportal-running \
                        -p 3000:3000 \
                        -e PORT=3000 \
                        ${APP_IMAGE}:latest
                """
                echo ">>> Waiting for app to be ready..."
                sh """
                    for i in \$(seq 1 20); do
                        if curl -sf http://localhost:3000/health > /dev/null 2>&1; then
                            echo "App is ready!"
                            break
                        fi
                        echo "Waiting... attempt \$i"
                        sleep 3
                    done
                """
            }
        }

        stage('Build Test Image') {
            steps {
                echo ">>> Building Selenium test Docker image..."
                sh "docker build -f Dockerfile.test -t ${TEST_IMAGE}:latest ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo ">>> Executing 19 Selenium test cases..."
                sh "mkdir -p ${RESULTS_DIR}"
                sh """
                    docker run --rm \
                        --network host \
                        --name selenium-tests \
                        -e APP_URL=${APP_URL} \
                        -v ${RESULTS_DIR}:/app/test-results \
                        ${TEST_IMAGE}:latest || true
                """
            }
        }

        stage('Publish Report') {
            steps {
                echo ">>> Publishing HTML test report..."
                publishHTML(target: [
                    allowMissing         : true,
                    alwaysLinkToLastBuild: true,
                    keepAll              : true,
                    reportDir            : 'test-results',
                    reportFiles          : 'report.html',
                    reportName           : 'Selenium Test Report'
                ])
                archiveArtifacts artifacts: 'test-results/**/*',
                                 allowEmptyArchive: true
            }
        }

        stage('Teardown') {
            steps {
                echo ">>> Stopping app container..."
                sh "docker rm -f jobportal-running 2>/dev/null || true"
            }
        }
    }

    post {
        always {
            script {
                def status = currentBuild.currentResult ?: 'UNKNOWN'
                def icon   = (status == 'SUCCESS') ? '✅' : '❌'
                def toAddr = sh(
                    script: "git log -1 --pretty=format:'%ae' 2>/dev/null || echo 'qasimalik@gmail.com'",
                    returnStdout: true
                ).trim()

                emailext(
                    subject: "${icon} Jenkins | Job Portal | Build #${BUILD_NUMBER} | ${status}",
                    to: "${toAddr}, qasimalik@gmail.com",
                    mimeType: 'text/html',
                    attachmentsPattern: 'test-results/report.html',
                    body: """
<html><body style="font-family:Arial;color:#333;">
<h2 style="color:${status == 'SUCCESS' ? '#28a745' : '#dc3545'}">
  ${icon} Job Portal Pipeline &mdash; ${status}
</h2>
<table border="1" cellpadding="8" cellspacing="0"
       style="border-collapse:collapse;width:500px;">
  <tr><td><b>Build #</b></td><td>${BUILD_NUMBER}</td></tr>
  <tr><td><b>Status</b></td><td>${status}</td></tr>
  <tr><td><b>Duration</b></td><td>${currentBuild.durationString}</td></tr>
  <tr><td><b>Build URL</b></td>
      <td><a href="${BUILD_URL}">${BUILD_URL}</a></td></tr>
</table>
<p>Full HTML report is attached to this email.</p>
<p>View online:
  <a href="${BUILD_URL}Selenium_20Test_20Report/">Selenium Test Report</a>
</p>
</body></html>
                    """
                )
            }
        }
    }
}