pipeline {
    agent any
    
    tools {
        // 根据项目需要选择合适的工具
        maven 'Maven 3.8.1'
        jdk 'JDK 11'
    }
    
    environment {
        // 定义环境变量
        APP_NAME = "alert-bot"
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
        TIMESTAMP = sh(script: "date +%Y%m%d_%H%M%S", returnStdout: true).trim()
        ARTIFACT_VERSION = "1.0.${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    // 清理工作空间
                    deleteDir()
                    
                    // 检出代码
                    checkout scm
                    
                    // 显示检出的文件
                    sh 'ls -la'
                }
            }
            post {
                success {
                    echo "代码检出成功"
                }
                failure {
                    echo "代码检出失败"
                }
            }
        }
        
        stage('Sync Repository') {
            steps {
                script {
                    echo "开始同步仓库代码..."
                    
                    // 获取最新代码
                    sh '''
                        git fetch --all
                        git pull origin ${BRANCH_NAME}
                    '''
                    
                    // 显示当前分支和提交信息
                    sh '''
                        echo "当前分支: $(git branch --show-current)"
                        echo "最新提交: $(git log -1 --oneline)"
                    '''
                }
            }
        }
        
        stage('Code Analysis') {
            steps {
                script {
                    echo "代码分析..."

                    // 检查代码质量（根据项目类型调整）
                    sh '''
                        # 代码格式检查
                        # find . -name "*.py" -exec python -m py_compile {} \\; || true

                        # 代码风格检查（如果使用Python）
                        # pip install flake8
                        # flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

                        # 统计代码行数
                        echo "代码文件统计:"
                        find . -type f -name "*.py" -o -name "*.java" -o -name "*.js" -o -name "*.ts" | wc -l
                    '''
                }
            }
        }

        
        stage('Build') {
            steps {
                script {
                    echo "开始构建项目..."
                    
                    // 根据项目类型执行构建
                    sh '''
                        # 创建构建目录
                        mkdir -p build
                        
                        # Python项目示例
                        if [ -f "requirements.txt" ]; then
                            echo "检测到Python项目"
                            pip install -r requirements.txt
                            # 如果有setup.py
                            if [ -f "setup.py" ]; then
                                python setup.py build
                            fi
                        fi
                        
                        # Node.js项目示例
                        if [ -f "package.json" ]; then
                            echo "检测到Node.js项目"
                            npm install
                            npm run build
                        fi
                        
                        # Java/Maven项目示例
                        if [ -f "pom.xml" ]; then
                            echo "检测到Maven项目"
                            mvn clean compile
                        fi
                        
                        # Gradle项目示例
                        if [ -f "build.gradle" ]; then
                            echo "检测到Gradle项目"
                            ./gradlew build
                        fi
                    '''
                }
            }
            post {
                success {
                    echo "构建成功"
                }
                failure {
                    echo "构建失败"
                    archiveArtifacts artifacts: 'build/**/*', allowEmptyArchive: true
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo "运行测试..."
                    
                    sh '''
                        # Python测试示例
                        if [ -f "requirements-dev.txt" ]; then
                            pip install -r requirements-dev.txt
                        fi
                        
                        if [ -d "tests" ]; then
                            echo "运行单元测试..."
                            # python -m pytest tests/ -v
                        fi
                        
                        # JavaScript测试示例
                        if [ -f "package.json" ] && grep -q "test" package.json; then
                            echo "运行npm测试..."
                            # npm test
                        fi
                        
                        # Java测试示例
                        if [ -f "pom.xml" ]; then
                            echo "运行Maven测试..."
                            # mvn test
                        fi
                    '''
                }
            }
            post {
                always {
                    // 发布测试结果
                    publishTestResults testResultsPattern: 'target/surefire-reports/*.xml,test-results/**/*.xml'
                }
            }
        }
        
        stage('Package') {
            steps {
                script {
                    echo "开始打包..."
                    
                    // 创建打包目录
                    sh 'mkdir -p dist artifacts'
                    
                    // 根据项目类型进行打包
                    sh '''
                        # Python打包示例
                        if [ -f "setup.py" ]; then
                            echo "打包Python项目..."
                            python setup.py sdist bdist_wheel
                            cp dist/*.tar.gz artifacts/ || true
                            cp dist/*.whl artifacts/ || true
                        fi
                        
                        # Node.js打包示例
                        if [ -f "package.json" ]; then
                            echo "打包Node.js项目..."
                            npm pack
                            cp *.tgz artifacts/ || true
                        fi
                        
                        # Java打包示例
                        if [ -f "pom.xml" ]; then
                            echo "打包Maven项目..."
                            mvn package -DskipTests
                            find target -name "*.jar" -exec cp {} artifacts/ \\;
                            find target -name "*.war" -exec cp {} artifacts/ \\;
                        fi
                        
                        # 创建通用压缩包
                        echo "创建通用压缩包..."
                        tar -czf artifacts/${APP_NAME}-${ARTIFACT_VERSION}.tar.gz \
                            --exclude='.git' \
                            --exclude='node_modules' \
                            --exclude='target' \
                            --exclude='build' \
                            --exclude='dist' \
                            --exclude='*.log' \
                            .
                    '''
                    
                    // 显示打包结果
                    sh '''
                        echo "打包完成，产物列表:"
                        ls -la artifacts/
                    '''
                }
            }
            post {
                success {
                    echo "打包成功"
                    // 归档打包产物
                    archiveArtifacts artifacts: 'artifacts/**/*', allowEmptyArchive: false
                }
                failure {
                    echo "打包失败"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo "部署准备..."
                    
                    // 可以在这里添加部署逻辑
                    sh '''
                        echo "准备部署文件..."
                        # 部署逻辑根据实际需求添加
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "清理工作空间..."
                // 可选：清理构建产物以节省空间
                // sh 'rm -rf build dist target'
            }
        }
        
        success {
            script {
                echo "流水线执行成功!"
                // 发送成功通知
                sh '''
                    echo "构建 #${BUILD_NUMBER} 成功完成于 $(date)" > build-success.txt
                '''
            }
        }
        
        failure {
            script {
                echo "流水线执行失败!"
                // 发送失败通知
                sh '''
                    echo "构建 #${BUILD_NUMBER} 失败于 $(date)" > build-failure.txt
                '''
            }
        }
        
        cleanup {
            script {
                echo "执行清理工作..."
            }
        }
    }
}
