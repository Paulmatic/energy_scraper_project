pipeline {
    agent any

    triggers {
        cron('H/10 * * * *')
    }

    environment {
        DB_HOST = 'energy_postgres'
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

        stage('Start PostgreSQL Container') {
            steps {
                script {
                    sh '''
                    if [ "$(docker ps -aq -f name=${POSTGRES_CONTAINER})" ]; then
                        echo "PostgreSQL container already exists"
                        docker start ${POSTGRES_CONTAINER}
                    else
                        docker run -d --name ${POSTGRES_CONTAINER} \
                            --restart=always \
                            -e POSTGRES_USER=energy_user \
                            -e POSTGRES_PASSWORD=energy_pass \
                            -e POSTGRES_DB=energy_db \
                            -p 5432:5432 \
                            --network ${NETWORK_NAME} \
                            postgres:13
                    fi
                    '''

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
                    sh "docker network create ${NETWORK_NAME} || true"
                    sh "docker network connect ${NETWORK_NAME} ${POSTGRES_CONTAINER} || true"
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
