pipeline {
    agent any

    triggers {
        cron('H H * * *') // Run every 24 hours, spread out per agent
    }

    environment {
        DB_HOST = 'energy_postgres'       // Network alias used for DB connection
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
        POSTGRES_CONTAINER = 'postgres-container'
        PGADMIN_CONTAINER = 'energy_pgadmin'  // Added pgadmin container
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

        stage('Get PostgreSQL Credentials') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'postgres-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        env.DB_USER = DB_USER
                        env.DB_PASS = DB_PASS
                        echo "Retrieved DB credentials for user: ${env.DB_USER}"
                    }
                }
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

        stage('Start PostgreSQL and PGAdmin Containers') {
            steps {
                script {
                    // Start PostgreSQL container if not running
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
                            postgres:latest
                    fi
                    """
                    // Start PGAdmin container if not running
                    sh """
                    if [ "\$(docker ps -aq -f name=${PGADMIN_CONTAINER})" ]; then
                        echo "PGAdmin container already exists"
                        docker start ${PGADMIN_CONTAINER}
                    else
                        docker run -d --name ${PGADMIN_CONTAINER} \\
                            --network ${NETWORK_NAME} \\
                            --restart=always \\
                            -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \\
                            -e PGADMIN_DEFAULT_PASSWORD=admin1234 \\
                            -p 8082:80 \\
                            dpage/pgadmin4
                    fi
                    """
                    // Wait for containers to be fully ready
                    echo "Waiting for PostgreSQL and PGAdmin to be ready..."
                    sleep(90)
                }
            }
        }

        stage('Build Scraper Docker Image') {
            steps {
                script {
                    sh "docker build -t ${SCRAPER_IMAGE} ."
                }
            }
        }

        stage('Run Scraper') {
            steps {
                script {
                    // Ensure the PostgreSQL container is connected to the right network
                    sh "docker network connect ${NETWORK_NAME} ${POSTGRES_CONTAINER} || true"

                    sh """
                    docker run --rm --network ${NETWORK_NAME} \\
                        -e DB_HOST=${DB_HOST} \\
                        -e DB_PORT=${DB_PORT} \\
                        -e DB_NAME=${DB_NAME} \\
                        -e DB_USER=${DB_USER} \\
                        -e DB_PASS=${DB_PASS} \\
                        ${SCRAPER_IMAGE}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "PostgreSQL and PGAdmin containers will remain running for further access."
        }
        success {
            echo "Pipeline executed successfully. PostgreSQL and PGAdmin containers are still running."
        }
        failure {
            echo "Pipeline failed. Investigate logs for details."
        }
    }
}
