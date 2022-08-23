def podYaml = libraryResource './ci/pod-template.yml'

pipeline {
    agent {
        kubernetes {
          label 'npm-builder'
          yaml podYaml
        }
    }
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        stage('Test') {
            steps {
                sh './jenkins/scripts/test.sh'
            }
        }
        stage('Preview environment') {
          when {
            allOf {
              not { triggeredBy 'EventTriggerCause' }
              branch 'pr-*'
              anyOf {
                changeset "${changesetDir}/**"
                triggeredBy 'UserIdCause'
              }
            }
        }
        stage('Deliver') {
            steps {
                sh './jenkins/scripts/deliver.sh'
                input message: 'Finished using the web site? (Click "Proceed" to continue)'
            }
        }
    }
  }
}