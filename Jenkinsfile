pipeline {
    agent any

    triggers {
        cron('H/10 * * * *') // Run every 10 minutes, spread out per agent
    }

    environment {
        DB_HOST = 'energy_postgres'       // Network alias used for DB connection
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
        DB_USER = credentials('postgres-credentials') // Using the credentials ID
        DB_PASS = credentials('postgres-credentials') // Using the credentials ID
        POSTGRES_CONTAINER = 'postgres-container'
        SCRAPER_IMAGE = 'energy-scraper:latest'
        NETWORK_NAME = 'energy-net'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Paulmatic/energy_scraper_project.git',
                    credentialsId: 'github-credentials'
            }
        }

        stage('Create Docker Network') {
            steps {
                script {
                    def networkExists = sh(script: "docker network ls --filter name=${NETWORK_NAME} -q", returnStdout: true).trim()
                    if (!networkExists) {
                        echo "Creating Docker network ${NETWORK_NAME}..."
                        sh "docker network create ${NETWORK_NAME}"
                    } else {
                        echo "Docker network ${NETWORK_NAME} already exists."
                    }
                }
            }
        }

        stage('Start PostgreSQL Container') {
            steps {
                script {
                    sh """
                    if [ "\$(docker ps -aq -f name=${POSTGRES_CONTAINER})" ]; then
                        echo "PostgreSQL container already exists"
                        docker start ${POSTGRES_CONTAINER}
                    else
                        docker run -d --name ${POSTGRES_CONTAINER} \\
                            --network ${NETWORK_NAME} \\
                            --network-alias ${DB_HOST} \\
                            --restart=always \\
                            -e POSTGRES_USER=${DB_USER} \\
                            -e POSTGRES_PASSWORD=${DB_PASS} \\
                            -e POSTGRES_DB=${DB_NAME} \\
                            -p ${DB_PORT}:${DB_PORT} \\
                            postgres:13
                    fi
                    """

                    sh '''
                    echo "Waiting for PostgreSQL to be ready..."
                    for i in {1..15}; do
                        if docker exec ${POSTGRES_CONTAINER} pg_isready -U ${DB_USER}; then
                            echo "PostgreSQL is ready."
                            break
                        fi
                        sleep 2
                    done
                    '''
                }
            }
        }

        stage('Run Scraper') {
            steps {
                script {
                    // Ensure the PostgreSQL container is connected to the right network
                    sh "docker network connect ${NETWORK_NAME} ${POSTGRES_CONTAINER} || true"

                    sh '''
                    docker run --rm --network ${NETWORK_NAME} \\
                        -e DB_HOST=${DB_HOST} \\
                        -e DB_PORT=${DB_PORT} \\
                        -e DB_NAME=${DB_NAME} \\
                        -e DB_USER=${DB_USER} \\
                        -e DB_PASS=${DB_PASS} \\
                        ${SCRAPER_IMAGE}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "PostgreSQL container will remain running for further access."
        }
        success {
            echo "Pipeline executed successfully. PostgreSQL container is still running."
        }
        failure {
            echo "Pipeline failed. Investigate logs for details."
        }
    }
}
