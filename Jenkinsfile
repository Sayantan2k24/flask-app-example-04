pipeline {
    agent any
    environment {
        DOCKER_USERNAME = 'sayantan2k21'
        APP_NAME = 'crickbuzz-api-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKER_USERNAME}/${APP_NAME}"


    }

    stages{

        stage('Clean the WS') {

            steps {
                            
                script{
                    cleanWs()
                }
            }

        }

        stage('Checkout SCM') {
            steps {
                git branch: 'main', credentialsId: 'git-cred', url: 'https://github.com/Sayantan2k24/flask-app-example-04-crickbuzz-api.git'
            }

        }

        stage('Build Image Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                """
            }

            
            
        }

        stage('Push The Image') {
            
            steps{
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-cred', passwordVariable: 'pass', usernameVariable: 'user')]) {
                        
                        sh """

                            echo  ${pass} | docker login -u ${user} --password-stdin

                            docker push ${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${IMAGE_NAME}:latest

                        """
                    }
                }


            }

        }

        stage('Delete Image Locally') {

            steps {
                sh """
                    docker rmi -f ${IMAGE_NAME}:${IMAGE_TAG}
                    docker rmi -f ${IMAGE_NAME}:latest
                """


            }

            
        }


        stage('Update the deployment file in CD') {

            steps {
                script{
                    withCredentials([usernamePassword(credentialsId: 'git-cred', passwordVariable: 'pass', usernameVariable: 'user')]) {


                        sh """
                            git clone -b main https://${pass}@github.com/Sayantan2k24/flask-app-example-04-crickbuzz-api-CD.git
                            cd flask-app-example-04-crickbuzz-api-CD

                            ls
                            cat deployment.yaml
                

                        """

                        sh """
                            echo "new shell"
                            echo $pwd
                            cd flask-app-example-04-crickbuzz-api-CD
                            echo $pwd

                            ls

                            cat deployment

                            echo "Changing tag to ${BUILD_NUMBER}"

                            sed -i 's|image: sayantan2k21/crickbuzz-api-app:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g' deployment.yaml

                            echo "changed tag:"

                            cat deployment


                            git add depoloyment.yaml
                            git commit -m "Updated the tag to ${BUILD_NUMBER}"
                            git push origin main

                        """

                    }

                }
            }
        }

        stage('Create ArgoCD Aplication from manifest') {
            steps {

                sh "kubectl apply -f application-argocd.yml"
            }
        }
    }       
}