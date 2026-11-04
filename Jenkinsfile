pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Construyendo proyecto Byebye Mundo...'
                sh 'mkdir -p build'
                sh 'cp app.py build/app.py'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas del proyecto...'
                sh 'grep -q "Byeee, DevSecOps!" build/app.py'
                echo 'Pruebas exitosas!'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Desplegando aplicación...'
                sh 'cat build/app.py'
                echo 'Despliegue de prueba completado!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado correctamente! Byeeee'
        }
        failure {
            echo 'El pipeline presentó un error.'
        }
    }
}