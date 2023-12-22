    def userGit = "pmbibe"
    def userDocker = "babibe2211"
    def repository = "https://github.com/pmbibe/db"
    def dockerRegistry = "https://registry.hub.docker.com"
    def branch = "main"
    def prj = "db-oracle-tool"
    def dockerBuildLabel = "builder"
    node("jenkins-agent") {
            stage("Pull code from GitLab"){
                    git branch: "${branch}", credentialsId: "${userGit}", url: "${repository}"
            }
            stage ("Build image") {
                customImage = docker.build("${userDocker}/${prj}:${BUILD_ID}", "--no-cache --build-arg buildArg=${BUILD_ID} .")
             
            }
            stage ("Clear image") {
                env.builderLabel = dockerBuildLabel
                sh '''
                    docker image rm $(docker images --filter "label=stage=${builderLabel}" --filter "label=builID=${BUILD_ID}" | awk 'FNR == 2 {print $3}')
                '''
            }
            stage ("Push image") {
                withDockerRegistry([url: "", credentialsId: "${userDocker}"]) {
                customImage.push()   
                }
            stage ("Clear all") {
                env.user = userDocker
                env.project = prj
                sh '''
                    docker image rm ${user}/${project}:${BUILD_ID}
                '''
            }
            }
