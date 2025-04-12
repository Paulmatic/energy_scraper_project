pipeline {
    agent any

    environment {
        NETWORK_NAME = 'energy-net'
        POSTGRES_CONTAINER = 'postgres-container'
        POSTGRES_USER = 'energy_user'
        POSTGRES_PASSWORD = 'energy_pass'
        POSTGRES_DB = 'energy_db'
        POSTGRES_HOST = 'energy_postgres'  // Alias for PostgreSQL container
    }

    stages {
        stage('Prepare Docker Network') {
            steps {
                script {
                    // Create Docker network if it doesn't exist
                    sh '''
                    if ! docker network inspect ${NETWORK_NAME} > /dev/null 2>&1; then
                        echo "Creating Docker network ${NETWORK_NAME}"
                        docker network create ${NETWORK_NAME}
                    else
                        echo "Network ${NETWORK_NAME} already exists."
                    fi
                    '''
                }
            }
        }

        stage('Start PostgreSQL Container') {
            steps {
                script {
                    // Start PostgreSQL container if not running
                    sh '''
                    if [ "$(docker ps -aq -f name=${POSTGRES_CONTAINER})" ]; then
                        echo "PostgreSQL container already exists"
                        docker start ${POSTGRES_CONTAINER}
                    else
                        echo "Starting PostgreSQL container"
                        docker run -d --name ${POSTGRES_CONTAINER} \
                            --network ${NETWORK_NAME} \
                            --network-alias ${POSTGRES_HOST} \
                            --restart=always \
                            -e POSTGRES_USER=${POSTGRES_USER} \
                            -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                            -e POSTGRES_DB=${POSTGRES_DB} \
                            -p 5432:5432 \
                            postgres:13
                    fi
                    '''

                    // Wait for PostgreSQL container to be ready
                    sh '''
                    echo "Waiting for PostgreSQL to be ready..."
                    for i in {1..15}; do
                        if docker exec ${POSTGRES_CONTAINER} pg_isready -U ${POSTGRES_USER}; then
                            echo "PostgreSQL is ready."
                            break
                        fi
                        sleep 2
                    done
                    '''
                }
            }
        }

        stage('Check Network Connection') {
            steps {
                script {
                    // Check if the PostgreSQL container is connected to the network
                    def connected = sh(script: "docker network inspect ${NETWORK_NAME} --format '{{range .Containers}}{{.Name}}{{end}}' | grep -w ${POSTGRES_CONTAINER} || true", returnStdout: true).trim()
                    if (!connected) {
                        echo "Connecting PostgreSQL container to network ${NETWORK_NAME}..."
                        sh "docker network connect ${NETWORK_NAME} ${POSTGRES_CONTAINER}"
                    } else {
                        echo "PostgreSQL container is already connected to the network ${NETWORK_NAME}"
                    }
                }
            }
        }

        stage('Run Scraper') {
            steps {
                script {
                    // Run the scraper container, ensuring it uses the same network and the alias for PostgreSQL
                    sh 'docker run --rm --network ${NETWORK_NAME} -e DB_HOST=${POSTGRES_HOST} energy-scraper:latest'
                }
            }
        }
    }

    post {
        always {
            // Optional: Clean up Docker containers after the pipeline is finished
            sh '''
            echo "Cleaning up containers..."
            docker rm -f ${POSTGRES_CONTAINER} || true
            '''
        }
    }
}
