pipeline {
    agent any

    environment {
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'energy_db'
    }

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/Paulmatic/energy_scraper_project.git', credentialsId: 'github-credentials'
            }
        }

        stage('Start PostgreSQL Docker Container') {
            steps {
                script {
                    // Run PostgreSQL container
                    sh 'docker ps -a -q -f name=postgres-container || docker run --name postgres-container -e POSTGRES_PASSWORD=energy_pass -e POSTGRES_USER=energy_user -d -p 5432:5432 postgres:latest'
                    
                    // Wait for the PostgreSQL container to be ready
                    sh '''
                    for i in {1..10}
                    do
                        nc -zv localhost 5432
                        if [ $? -eq 0 ]; then
                            echo "PostgreSQL is ready"
                            break
                        fi
                        sleep 1
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
                withCredentials([usernamePassword(credentialsId: 'postgres-credentials', usernameVariable: 'DB_USERNAME', passwordVariable: 'DB_PASSWORD')]) {
                    script {
                        // Print DB credentials to verify (avoid printing in real environments)
                        echo "DB_USER=${DB_USERNAME}"
                        echo "DB_PASSWORD=${DB_PASSWORD}"

                        // Set environment variables for DB connection
                        sh """
                        export DB_HOST=localhost
                        export DB_PORT=5432
                        export DB_NAME=energy_db
                        python3 scrape_energy_data.py
                        """
                    }
                }
            }
        }
    }
}
