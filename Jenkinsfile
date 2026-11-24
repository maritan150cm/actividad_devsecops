pipeline {
    agent any

    environment {
        APP_IMAGE = "actividad-devsecops:${BUILD_NUMBER}"
        TEST_CONTAINER = "actividad-devsecops-test"
        DEPLOY_CONTAINER = "actividad-devsecops-app"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Construyendo la imagen Docker...'
                sh 'docker build -t actividad-devsecops:${BUILD_NUMBER} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Comprobando que la aplicacion inicia correctamente...'
                sh '''
                    docker rm -f ${TEST_CONTAINER} 2>/dev/null || true
                    docker run -d --name ${TEST_CONTAINER} --network devsecops-net ${APP_IMAGE}
                    sleep 5
                    docker exec ${TEST_CONTAINER} python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/').read().decode())"
                    docker rm -f ${TEST_CONTAINER}
                '''
            }
        }

        stage('Documentation') {
            steps {
                echo 'Generando documentacion del proyecto con Doxygen...'
                sh 'docker run --rm --volumes-from jenkins -w "$WORKSPACE" nakatt/doxygen Doxyfile'
                echo 'Documentacion HTML generada correctamente.'
            }
        }

        stage('Analyze') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=actividad_devsecops \
                            -Dsonar.projectName=actividad_devsecops \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions=**/build/**,**/.git/**
                        """
                    }
                }
            }
        }

        
        stage('Security Test') {
            steps {
                echo 'Analizando dependencias con OWASP Dependency-Check...'

                sh 'mkdir -p dependency-check-reports'

                dependencyCheck(
                    additionalArguments: '--enableExperimental --scan . --format XML --format HTML --out dependency-check-reports',
                    odcInstallation: 'Dependency-Check',
                    nvdCredentialsId: 'nvd-api-key'
                )  

                dependencyCheckPublisher(
                    pattern: 'dependency-check-reports/dependency-check-report.xml'
                )

                echo 'Ejecutando analisis de seguridad con OWASP ZAP...'

                sh '''
                    docker rm -f ${TEST_CONTAINER} 2>/dev/null || true
                    docker run -d --name ${TEST_CONTAINER} --network devsecops-net ${APP_IMAGE}
                    sleep 5
                '''

                script {
                    def zapStatus = sh(
                        script: 'docker run --rm --network devsecops-net --volumes-from jenkins -v jenkins_home:/zap/wrk -w "$WORKSPACE" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://${TEST_CONTAINER}:5000 -r workspace/actividad-3-2-2-devsecops/zap-report.html',
                        returnStatus: true
                    )

                    if (zapStatus != 0 && zapStatus != 2) {
                        error "ZAP termino con codigo ${zapStatus}. Revisa el registro."
                    }

                    if (zapStatus == 2) {
                        echo 'ZAP termino con advertencias. Revisa el informe.'
                    } else {
                        echo 'ZAP termino sin advertencias.'
                    }
                }

                sh 'docker rm -f ${TEST_CONTAINER} 2>/dev/null || true'
            }
        }


        stage('Deploy') {
            steps {
                echo 'Desplegando aplicacion en entorno de prueba...'
                sh '''
                    docker rm -f ${DEPLOY_CONTAINER} 2>/dev/null || true
                    docker run -d --name ${DEPLOY_CONTAINER} --network devsecops-net -p 5000:5000 ${APP_IMAGE}
                '''
                echo 'aplicacion desplegada en el puerto 5000.'
            }
        }
    }

    post {
        always {
            sh 'docker rm -f ${TEST_CONTAINER} 2>/dev/null || true'
        }
        success {
            echo 'Pipeline DevSecOps ejecutado correctamente.'
        }
        failure {
            echo 'El pipeline presento un error. Revisa los registros de ejecucion.'
        }
    }
}


