node {
    checkout scm
    stage("Build Artifact") {
        sh("arm build")
        sh("arm unit")
    }
    stage("Promote Artifact") {
        sh("arm release")
    }
}
