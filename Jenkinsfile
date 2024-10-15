pipeline {
    agent any

    environment {
        SQLDB_URL = "sqlite+aiosqlite:///./test-data/test-sqlalchemy.db"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/bmyaye/Mood-Tracker-Backend'
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                    args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            environment {
                SQLDB_URL = "sqlite+aiosqlite:///./test-data/test-sqlalchemy.db"
            }
            steps {
                dir('snoutsaver') {
                    sh "pip install poetry"
                    sh "poetry config virtualenvs.in-project true"
                    sh "poetry install"
                    
                    // สร้าง directory สำหรับรายงานการทดสอบ
                    sh "mkdir -p ../test-reports"
                    
                    // เช็คไฟล์ทดสอบ
                    sh "echo 'Listing snoutsaver directory:'"
                    sh "ls -R"

                    // รัน pytest และสร้างรายงานในรูปแบบ JUnit XML
                    sh "poetry run pytest -v /tests/ --junitxml=../test-reports/results.xml"

                    // เช็คว่าไฟล์รายงานถูกสร้างขึ้นมา
                    sh "echo 'Listing test-reports directory:'"
                    sh "ls -l ../test-reports/"
                }
            }
        }
    }

    post {
        always {
            junit 'test-reports/results.xml'
            cleanWs()
        }
    }
}
