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
        
        // Virtual environments used to ensure a clean install on each run
        stage ('Set up Virtual Environment') {
            steps {
                sh '''
                    echo ${SHELL}
                    [ -d venv ] && rm -rf venv
                    virtualenv venv --python=python3.5
                '''
            }
        }

        stage ('Install Requirements') {
            steps {
                sh '''
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
                    pytest tests/unit/test_*
                '''
            }
        }

    }

}