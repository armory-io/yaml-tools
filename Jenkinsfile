node {
    checkout scm
    stage("Build Artifact") {
        //sh("arm build")
        //sh("arm unit")
    }
    stage("Promote Artifact") {
      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'armory-jenkins', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        sh("arm release")
      }
    }
}
