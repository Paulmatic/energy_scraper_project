pipeline {
    agent any

    environment {
        DB_USERNAME = credentials('postgres-username')  // Jenkins secret ID
        DB_PASSWORD = credentials('postgres-password')
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'postgres'
    }

    triggers {
        cron('H 6 * * *')  // Runs daily at ~6 AM (randomized minute)
    }

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/Paulmatic/python-dump.git', branch: 'main'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Scraper Script') {
            steps {
                sh 'python3 scrape_energy_data.py'
            }
        }

        stage('Archive CSV') {
            steps {
                archiveArtifacts artifacts: 'data/energy_intelligence.csv', onlyIfSuccessful: true
            }
        }
    }
}
