pipeline {
    agent any

    environment {
        // Environment Variables for PostgreSQL credentials
        DB_HOST = 'energy_postgres'
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
        DB_USER = credentials('postgres-username')  // Jenkins credential for DB user
        DB_PASS = credentials('postgres-password')  // Jenkins credential for DB password
        DOCKER_IMAGE = 'energy-scraper:latest'
        NETWORK = 'energy-net'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone your Git repository
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        // Building Docker image
                        echo "Building Docker image: ${DOCKER_IMAGE}"
                        sh "docker build -t ${DOCKER_IMAGE} ."
                    } catch (Exception e) {
                        echo "Failed to build Docker image."
                        throw e  // Fail the pipeline if the build fails
                    }
                }
            }
        }

        stage('Run PostgreSQL Container') {
            steps {
                script {
                    try {
                        // Running PostgreSQL container
                        echo "Running PostgreSQL container"
                        sh """
                            docker run --rm --network ${NETWORK} \
                                -e DB_HOST=${DB_HOST} \
                                -e DB_PORT=${DB_PORT} \
                                -e DB_NAME=${DB_NAME} \
                                -e DB_USER=${DB_USER} \
                                -e DB_PASS=${DB_PASS} \
                                ${DOCKER_IMAGE}
                        """
                    } catch (Exception e) {
                        echo "Failed to run PostgreSQL container."
                        throw e
                    }
                }
            }
        }

        stage('Run Scraper') {
            steps {
                script {
                    try {
                        // Running the scraper application
                        echo "Running the scraper with the PostgreSQL environment"
                        sh """
                            docker run --rm --network ${NETWORK} \
                                -e DB_HOST=${DB_HOST} \
                                -e DB_PORT=${DB_PORT} \
                                -e DB_NAME=${DB_NAME} \
                                -e DB_USER=${DB_USER} \
                                -e DB_PASS=${DB_PASS} \
                                ${DOCKER_IMAGE}
                        """
                    } catch (Exception e) {
                        echo "Failed to run scraper."
                        throw e
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Perform cleanup if needed
                    echo "Cleaning up the environment..."
                    sh 'docker system prune -f'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for more details.'
        }
    }
}
