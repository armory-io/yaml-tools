node {
    checkout scm
    stage("Build Artifact") {
        sh("arm unit")
        archiveArtifacts artifacts: 'build/*', fingerprint: true
    }
    stage("Promote Artifact") {
        sh("arm release")
    }
}
