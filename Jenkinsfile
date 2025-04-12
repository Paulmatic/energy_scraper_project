pipeline {
    agent any

    triggers {
        cron('H/10 * * * *') // Run every 10 minutes, spread out per agent
    }

    environment {
        DB_HOST = 'energy_postgres'       // Network alias used for DB connection
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
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

        stage('Get PostgreSQL Credentials') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'postgres-credentials', usernameVariable: 'JENKINS_DB_USER', passwordVariable: 'JENKINS_DB_PASS')]) {
                        // Ensure the credentials are set properly before passing them to the environment
                        if (JENKINS_DB_USER && JENKINS_DB_PASS) {
                            env.DB_USER = JENKINS_DB_USER
                            env.DB_PASS = JENKINS_DB_PASS
                            echo "Retrieved DB credentials for user: ${env.DB_USER}"
                        } else {
                            error "DB credentials not found!"
                        }
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
                            postgres:latest
                    fi
                    """

                    sh """
                    echo "Waiting for PostgreSQL to be ready..."
                    for i in {1..15}; do
                        if docker exec ${POSTGRES_CONTAINER} pg_isready -U ${DB_USER}; then
                            echo "PostgreSQL is ready."
                            break
                        fi
                        sleep 120
                    done
                    """
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
                    // Securely pass credentials using environment variables directly to docker run
                    withCredentials([usernamePassword(credentialsId: 'postgres-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        // Ensure DB_USER and DB_PASS are set before running scraper
                        if (env.DB_USER && env.DB_PASS) {
                            echo "Running scraper with DB user: ${env.DB_USER}"
                            sh """
                            docker network connect ${NETWORK_NAME} ${POSTGRES_CONTAINER} || true

                            docker run --rm --network ${NETWORK_NAME} \\
                                -e DB_HOST=${DB_HOST} \\
                                -e DB_PORT=${DB_PORT} \\
                                -e DB_NAME=${DB_NAME} \\
                                -e DB_USER=${DB_USER} \\
                                -e DB_PASS=${DB_PASS} \\
                                ${SCRAPER_IMAGE}
                            """
                        } else {
                            error "DB_USER or DB_PASS is not set!"
                        }
                    }
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
