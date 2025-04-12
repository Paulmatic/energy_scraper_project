pipeline {
    agent any

    environment {
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'postgres'
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
                    sh '''
                        python3 scrape_energy_data.py
                    '''
                }
            }
        }

        stage('Archive CSV') {
            steps {
                archiveArtifacts artifacts: 'data/energy_intelligence.csv', onlyIfSuccessful: true
            }
        }
    }
}
