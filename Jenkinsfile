pipeline {
    
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr:'10'))
    }

    environment {
        projectName = 'scr'
        VIRTUAL_ENV = "${env.WORKSPACE}/venv"
    }

    stages {

        stage ('Install Requirements') {
            steps {
                sh '''
                    echo ${SHELL}
                    [ -d venv ] && rm -rf venv
                    virtualenv venv --python=python3.5
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage ('Run Unit Tests') {
            steps {
                sh '''
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    py.test --cov=$(NAME) --junitxml $(REPORT_DIR)/pytest.xml --cov-report html:$(REPORT_DIR)/coverage/index.html tests/unit/*
                '''
            }

            post {
                always {
                    junit keepLongStdio: true, testResults: 'report/pytext.xml'
                    publishHTML target: [
                        reportDir: 'report/coverage',
                        reportFiles: 'index.hmtl',
                        reportName: 'Coverage Report - Unit Test'
                    ]
                }
            }
        }

        stage ('Cleanup') {
            steps {
                sh 'rm -rf venv'
            }
        }

    }

}