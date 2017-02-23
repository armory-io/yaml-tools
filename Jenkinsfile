node {
    checkout scm
    stage("Build Artifact") {
        sh("arm build")
        sh("arm unit")
    }
    stage("Promote Artifact") {
      sh('env')
      sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@<REPO> --tags')
    }
}
