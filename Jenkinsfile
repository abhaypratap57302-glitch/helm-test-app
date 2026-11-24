pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'abhaygoku/helm-test'
        IMAGE_TAG      = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} .'
            }
        }

        stage('Smoke test') {
            steps {
                // Start the container on host port 5001 and check the /health endpoint
                sh '''
                    docker run -d --name smoke-${BUILD_NUMBER} -p 5001:5000 ${DOCKERHUB_REPO}:${IMAGE_TAG}
                    sleep 5
                    curl -f http://localhost:5001/health
                '''
            }
            post {
                always {
                    sh 'docker rm -f smoke-${BUILD_NUMBER} || true'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success {
            echo "Pushed ${DOCKERHUB_REPO}:${IMAGE_TAG}"
        }
    }
}
