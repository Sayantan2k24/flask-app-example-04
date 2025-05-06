pipeline {
    agent any

    environment {
        DOCKER_USERNAME = "sayantan2k21"
        APP_NAME = 'crickbuzz-api-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKER_USERNAME}/${APP_NAME}"
    }

    stages {

        stage('Clean The workspace') {

            steps {

                script {

                    cleanWs()
                }
            }
        }

        stage('Checkout Git Scm') {

            steps{
                git branch: 'main', credentialsId: 'git-cred', url: 'https://github.com/Sayantan2k24/flask-app-example-04-crickbuzz-api.git'

            }
        }

        stage('Build the Docker image') {

            steps {

                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} . "
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG}  ${IMAGE_NAME}:latest"
            }
        }

        stage('Push the Image to DockerHub') {


            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-cred', passwordVariable: 'pass', usernameVariable: 'user')]) {
                // some block
                    sh """
                    
                        echo ${pass} | docker login -u ${DOCKER_USERNAME} --password-stdin

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest


                    """
            }

            }
            

        }

        stage('Delete the Image Locally') {

            steps {
                sh """
                    docker rmi -f ${IMAGE_NAME}:${IMAGE_TAG}
                    docker rmi -f ${IMAGE_NAME}:latest

                """

            }
        }

        stage('Update the deployment file in CD repo') {

            steps {


                withCredentials([usernamePassword(credentialsId: 'git-cred', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    // some block
                    sh """
                        git clone -b main https://${pass}@github.com/Sayantan2k24/flask-app-example-04-crickbuzz-api-CD.git

                        cd flask-app-example-04-crickbuzz-api-CD

                        ls

                        cat deployment.yaml

                        sed -i "s|image: sayantan2k21/crickbuzz-api-app:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g" deployment.yaml

                        cat deployment.yaml

                        git add deployment.yaml
                        git commit -m "Updated the tag with ${IMAGE_TAG}"

                        git push origin main
                
                """
                }

            }
        }

        stage("Create Argocd Application") {
            steps {

                sh "echo $pwd"

                sh "kubectl apply -f application-argocd.yml "
            }
        }

    }

}