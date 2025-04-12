pipeline {
    agent any

    environment {
        DB_HOST = 'localhost' // Use 'localhost' for the Docker container setup
        DB_PORT = '5432'
        DB_NAME = 'energy_db'  // Adjust the database name to match your setup
        DB_USERNAME = 'energy_user' // Match your .env file values
        DB_PASSWORD = 'energy_pass' // Match your .env file values
    }

    triggers {
        cron('H 6 * * *') // Runs daily at a randomized minute past 6 AM
    }

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/Paulmatic/energy_scraper_project.git', branch: 'main'
            }
        }

        stage('Start PostgreSQL Docker Container') {
            steps {
                script {
                    // Check if the PostgreSQL container exists
                    def containerExists = sh(script: "docker ps -a -q -f name=postgres-container", returnStdout: true).trim()
                    if (containerExists) {
                        echo "PostgreSQL container already exists."
                    } else {
                        // Pull and run the PostgreSQL Docker container if it doesn't exist
                        sh 'docker run --name postgres-container -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_USER=$DB_USERNAME -d -p 5432:5432 postgres:latest'
                    }

                    // Wait for PostgreSQL to be fully ready before proceeding
                    sh '''
                        for i in {1..10}; do
                            if nc -zv localhost 5432; then
                                echo "PostgreSQL is ready"
                                break
                            fi
                            echo "Waiting for PostgreSQL to start..."
                            sleep 5
                        done
                    '''
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Scraper Script with Secrets') {
            steps {
                withCredentials([
                    string(credentialsId: 'postgres-username', variable: 'DB_USERNAME'),
                    string(credentialsId: 'postgres-password', variable: 'DB_PASSWORD')
                ]) {
                    // Set environment variables and run the Python script
                    sh '''
                        echo 'DB_USER=$DB_USERNAME' > .env
                        echo 'DB_PASSWORD=$DB_PASSWORD' >> .env
                        echo 'DB_HOST=localhost' >> .env
                        echo 'DB_PORT=5432' >> .env
                        echo 'DB_NAME=energy_db' >> .env
                        python3 scrape_energy_data.py
                    '''
                }
            }
        }

        stage('Stop PostgreSQL Docker Container') {
            steps {
                // Stop and remove the container after execution
                sh 'docker stop postgres-container || true'
                sh 'docker rm postgres-container || true'
            }
        }

        stage('Archive CSV') {
            steps {
                archiveArtifacts artifacts: 'data/energy_intelligence.csv', onlyIfSuccessful: true
            }
        }
    }

    post {
        always {
            // Ensure the container is stopped and removed even if the pipeline fails
            script {
                try {
                    sh 'docker stop postgres-container || true'
                    sh 'docker rm postgres-container || true'
                } catch (Exception e) {
                    echo "Error while stopping or removing container: ${e.getMessage()}"
                }
            }
        }
    }
}
