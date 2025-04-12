pipeline {
    agent any

    triggers {
        cron('H/10 * * * *') // Run every 10 minutes, spread out per agent
    }

    environment {
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
        POSTGRES_CONTAINER = 'postgres-container'
        SCRAPER_IMAGE = 'energy-scraper:latest'
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
                    // Start Postgres only if not running
                    sh '''
                    if [ "$(docker ps -aq -f name=${POSTGRES_CONTAINER})" ]; then
                        echo "PostgreSQL container already exists"
                        docker start ${POSTGRES_CONTAINER}
                    else
                        docker run -d --name ${POSTGRES_CONTAINER} \
                            -e POSTGRES_USER=energy_user \
                            -e POSTGRES_PASSWORD=energy_pass \
                            -e POSTGRES_DB=energy_db \
                            -p 5432:5432 postgres:13
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

        stage('Run Scraper Inside Docker') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'postgres-credentials', usernameVariable: 'DB_USERNAME', passwordVariable: 'DB_PASSWORD')]) {
                    script {
                        sh """
                        docker run --rm --network host \
                            -e DB_USERNAME=${DB_USERNAME} \
                            -e DB_PASSWORD=${DB_PASSWORD} \
                            -e DB_HOST=${DB_HOST} \
                            -e DB_PORT=${DB_PORT} \
                            -e DB_NAME=${DB_NAME} \
                            ${SCRAPER_IMAGE}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker containers..."
            sh 'docker stop ${POSTGRES_CONTAINER} || true'
            sh 'docker rm ${POSTGRES_CONTAINER} || true'
        }
    }
}
