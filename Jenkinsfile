def podYaml = libraryResource './ci/pod-template.yml'
def repoOwner = env.
def repo = env.
def githubCredentialId = env.

pipeline {
    agent {
        kubernetes {
          label 'npm-builder'
          yaml podYaml
        }
    }
    environment {
        CI = 'true'
        repoOwner = "${repoOwner}"
        repo = "${repo}"
        githubCredentialId = "${githubCredentialId}"
        credId = "${githubCredentialId}"
    }
    stages {
        stage('echo envs') {
            steps {
              echo "env:  ${env.getEnvironment()}"
            }
        }
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
              stages {
                stage("Build site") {
                  steps {
                    gitHubDeploy(repoOwner, repo, "", "${projectName} preview", "${githubCredentialId}", "true", "false")
                    sh "git submodule update --init"
                    dir("${sourceDir}") {
                      container('hugo') {
                        sh "hugo --config ${config} --contentDir ${contentDir}"
                        stash name: "public", includes: "public/**,Dockerfile,nginx/**"
                      }
                    }
                  }
                }
                stage("Build and push image") {
                  steps {
                    containerBuildPushGeneric("${projectName}", "${BRANCH_NAME.toLowerCase()}", "${gcpProject}"){
                      unstash "public"
                    }
                  }
                }
                stage("Deploy Preview") {
                  steps {
                    cloudRunDeploy(serviceName: "${projectName}-${BRANCH_NAME.toLowerCase()}", image: "gcr.io/${gcpProject}/${projectName}:${BRANCH_NAME.toLowerCase()}", deployType: "${deployTypePR}", region: "${gcpRegionPR}", clusterName: "${clusterNamePR}", namespace: "${namespacePR}")
                  }
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