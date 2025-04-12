pipeline {
    agent any

    triggers {
        cron('H/10 * * * *') // Run every 10 minutes, spread out per agent
    }

    environment {
        DB_HOST = 'postgres-container'  // Use the container name instead of 'energy_postgres'
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
        POSTGRES_CONTAINER = 'postgres-container'
        SCRAPER_IMAGE = 'energy-scraper:latest'
        NETWORK_NAME = 'energy-net'  // Use the same network for both containers
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Paulmatic/energy_scraper_project.git',
                    credentialsId: 'github-credentials'
            }
        }

        stage('Start PostgreSQL Container') {
            steps {
                script {
                    // Start Postgres only if not running, with network alias
                    sh '''
                    if [ "$(docker ps -aq -f name=${POSTGRES_CONTAINER})" ]; then
                        echo "PostgreSQL container already exists"
                        docker start ${POSTGRES_CONTAINER}
                    else
                        docker run -d --name ${POSTGRES_CONTAINER} \
                            --network ${NETWORK_NAME} \
                            --network-alias energy_postgres \
                            --restart=always \
                            -e POSTGRES_USER=energy_user \
                            -e POSTGRES_PASSWORD=energy_pass \
                            -e POSTGRES_DB=energy_db \
                            -p 5432:5432 \
                            postgres:13
                    fi
                    '''

                    // Wait until PostgreSQL is accepting connections
                    sh '''
                    echo "Waiting for PostgreSQL to be ready..."
                    for i in {1..15}; do
                        if docker exec ${POSTGRES_CONTAINER} pg_isready -U energy_user; then
                            echo "PostgreSQL is ready."
                            break
                        fi
                        sleep 2
                    done
                    '''
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
                    // Check if the Docker network exists; if not, create it
                    def networkExists = sh(script: "docker network ls --filter name=${NETWORK_NAME} -q", returnStdout: true).trim()
                    if (!networkExists) {
                        echo "Creating Docker network ${NETWORK_NAME}..."
                        sh "docker network create ${NETWORK_NAME}"
                    }

                    // Ensure the PostgreSQL container is connected to the network
                    sh "docker network connect ${NETWORK_NAME} ${POSTGRES_CONTAINER} || true"
                    
                    // Run the scraper container connected to the same network
                    sh '''
                        docker run --rm --network ${NETWORK_NAME} ${SCRAPER_IMAGE}
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
    }
}
