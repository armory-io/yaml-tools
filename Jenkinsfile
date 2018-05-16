node {
    checkout scm
    stage("Build Artifact") {
        sh("arm build")
        sh("arm unit")
    }
    stage("Promote Artifact") {
      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'd97828c0-7c09-4205-be6c-bd5395b704aa', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        sh("arm release")
      }
    }
}
