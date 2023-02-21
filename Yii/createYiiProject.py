# Import mudules
import os
import time
from datetime import datetime
start_time = time.time()

def main():
    # Giving the user options
    directory = input('Please enter your project directory:\n')
    projectName = input('Please enter the desired project name: ')
    databaseName = input('Please enter your database name (optional): ')
    print("Please verify these changes: \n\nInstallation directory: " + directory + "\nProject name: " + projectName + "\nDatabase name: " + databaseName + "\n\n")
    acceptChanges = input("Do you accept these changes? [y/n]")

    if acceptChanges == 'y':
        print("Starting the download of Yii in the desired directory")

        db_config = """<?php

        return [
            'class' => 'yii\db\Connection',
            'dsn' => 'mysql:host=localhost;dbname=""" + projectName +"""',
            'username' => 'root',
            'password' => '',
            'charset' => 'utf8',

            // Schema cache options (for production environment)
            //'enableSchemaCache' => true,
            //'schemaCacheDuration' => 60,
            //'schemaCache' => 'cache',
        ];"""

        db_config_dbname = """<?php

        return [
            'class' => 'yii\db\Connection',
            'dsn' => 'mysql:host=localhost;dbname=""" + databaseName +"""',
            'username' => 'root',
            'password' => '',
            'charset' => 'utf8',

            // Schema cache options (for production environment)
            //'enableSchemaCache' => true,
            //'schemaCacheDuration' => 60,
            //'schemaCache' => 'cache',
        ];"""

        web_php = r"""<?php

        $params = require __DIR__ . '/params.php';
        $db = require __DIR__ . '/db.php';

        $config = [
            'id' => 'basic',
            'basePath' => dirname(__DIR__),
            'bootstrap' => ['log'],
            'aliases' => [
                '@bower' => '@vendor/bower-asset',
                '@npm'   => '@vendor/npm-asset',
            ],
            'components' => [
                'request' => [
                    // !!! insert a secret key in the following (if it is empty) - this is required by cookie validation
                    'cookieValidationKey' => 'OezOTwisvvJzcFiIIUi8pAYarQWqsQeh',
                ],
                'cache' => [
                    'class' => 'yii\caching\FileCache',
                ],
                'user' => [
                    'identityClass' => 'app\models\User',
                    'enableAutoLogin' => true,
                ],
                'errorHandler' => [
                    'errorAction' => 'site/error',
                ],
                'mailer' => [
                    'class' => \yii\symfonymailer\Mailer::class,
                    'viewPath' => '@app/mail',
                    // send all mails to a file by default.
                    'useFileTransport' => true,
                ],
                'log' => [
                    'traceLevel' => YII_DEBUG ? 3 : 0,
                    'targets' => [
                        [
                            'class' => 'yii\log\FileTarget',
                            'levels' => ['error', 'warning'],
                        ],
                    ],
                ],
                'db' => $db,
                'urlManager' => [
                    'enablePrettyUrl' => true,
                    'showScriptName' => false,
                    'rules' => [
                    ],
                ],
            ],
            'params' => $params,
        ];

        if (YII_ENV_DEV) {
            // configuration adjustments for 'dev' environment
            $config['bootstrap'][] = 'debug';
            $config['modules']['debug'] = [
                'class' => 'yii\debug\Module',
                // uncomment the following to add your IP if you are not connecting from localhost.
                //'allowedIPs' => ['127.0.0.1', '::1'],
            ];

            $config['bootstrap'][] = 'gii';
            $config['modules']['gii'] = [
                'class' => 'yii\gii\Module',
                // uncomment the following to add your IP if you are not connecting from localhost.
                //'allowedIPs' => ['127.0.0.1', '::1'],
            ];
        }

        return $config;"""


        if len(databaseName) == 0:
            # Change directory to user desired directory
            os.chdir(directory)
            time.sleep(2)

            # install section
            os.system('composer create-project --prefer-dist yiisoft/yii2-app-basic ' + projectName)

            print("Using project name for as database name")
            os.chdir(directory+"/"+projectName)
            time.sleep(1)
            # Changing neccesary files 
            with open(r'config/db.php', "w") as f:
                f.write(db_config)
                print('Changed the db.php file in the ' +projectName+'/config/db.php')

            with open(r'config/web.php', "w") as f:
                f.write(web_php)
                print('Changed the db.php file in the ' +projectName+'/config/web.php')
        else: 
            # Change directory to user desired directory
            os.chdir(directory)
            time.sleep(2)

            # install section
            os.system('composer create-project --prefer-dist yiisoft/yii2-app-basic ' + projectName)

            print("Using database name for as database name")
            os.chdir(directory+"/"+projectName)
            time.sleep(1)
            # Changing neccesary files 
            with open(r'config/db.php', "w") as f:
                f.write(db_config_dbname)
                print('Changed the db.php file in the ' +projectName+'/config/db.php')

            with open(r'config/web.php', "w") as f:
                f.write(web_php)
                print('Changed the db.php file in the ' +projectName+'/config/web.php')

        # Get current time and 
        currentTime = datetime.now().strftime("%H:%M:%S")
        print('finished creating desired directories, happy coding!\n\nFinished at: ' + currentTime + '\nTotal duration: ' + "%s seconds" % (time.time() - start_time) + "\n\nStart Yii with the command: php yii serve")

    elif acceptChanges == 'n':
        exit()
    else:
        main()

main()