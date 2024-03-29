# Import mudules
import os
import re
import time
from datetime import datetime
from sys import platform
import platform
import subprocess
# import MySQLdb
import mysql.connector
import sqlite3
import json
import shutil

start_time = time.time()


# ----------------------------
# -                          -
# -        ELECTRON          -
# -                          -
# ----------------------------

def electron():
    index_js = """
    const { app, BrowserWindow, screen } = require("electron")

    let win = null;
    let loadingWindow = null;

    app.whenReady().then(() => {
        // Create the loading window
        loadingWindow = new BrowserWindow({
            width: 500,
            height: 300,
            transparent: true,
            frame: false,
            alwaysOnTop: true,
            // devTools: false,
            // icon: __dirname + './project files/icon/finished/icon.png'
        });
        loadingWindow.loadFile('./app/loading/index.html');
        loadingWindow.center();

        // Create the main window
        const primaryDisplay = screen.getPrimaryDisplay()
        const { width, height } = primaryDisplay.size
        if (width == 1920 && height == 1080) {
            createMainWindow(1280, 720)
        } else if (width == 1280 && height == 720) {
            createMainWindow(854, 480)
        } else {
            let widthDevided = width / 1.5;
            let heighDevided = height / 1.5;
            createMainWindow(widthDevided, heighDevided)
        }

        // Close the loading window and show the main window
        setTimeout(function() {
            loadingWindow.close();
            win.show();
        }, 3000);
    });

    function createMainWindow(winWidth, winHeight) {
        win = new BrowserWindow({
            width: winWidth,
            height: winHeight,
            show: false,
            resizable: true,
            // icon: __dirname + './project files/icon/finished/icon.png',
            webPreferences: {
                nodeIntegration: true,
                // devTools: false
            }
        })
        win.loadFile('./app/main/index.html')
        win.center();
    }
    """

    gitignore = """
    node_modules/
    *.xcf
    .env
    """

    gitconfig = """
    [safe]
        directory = *
    """

    logging_js = """
    const date = new Date();

    function fullLoad() {
        console.log(date + "Info:\n\nAll Content has been loaded succesfully");
    }
    """

    loading_index_html = """
    <html>

    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="./style.css">
        <title>title here</title>
    </head>

    <body>
        <h3>Application Is Starting...</h3>
        <div class="loader"></div>

    </html>
    """

    loading_style_css = """
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu&display=swap');
    * {
        font-family: 'Ubuntu', sans-serif;
    }

    body {
        background-color: #f9f9fa;
        background-image: url('./img/background.webp');
    }

    h3 {
        color: #fff;
    }

    .flex {
        -webkit-box-flex: 1;
        -ms-flex: 1 1 auto;
        flex: 1 1 auto
    }

    .loader {
        border: 5px solid rgba(18, 65, 145, 255);
        border-radius: 50%;
        border-top: 5px solid #ffffff;
        width: 40px;
        height: 40px;
        -webkit-animation: spin 1s linear infinite;
        /* Safari */
        animation: spin 1s linear infinite;
        margin: auto;
        left: 0;
        right: 0;
        top: 0px;
        bottom: 0;
        position: fixed;
    }


    /* Safari */

    @-webkit-keyframes spin {
        0% {
            -webkit-transform: rotate(0deg);
        }
        100% {
            -webkit-transform: rotate(360deg);
        }
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .center {
        border: none !important;
        text-align: center;
    }
    """

    main_index_html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>title here</title>
    </head>

    <body>
        <h1>Hello world!</h1>

        <script src="./scripts/script.js"></script>
    </body>

    </html>
    """

    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("Electron")
        print(ascii_banner)
    except ImportError as e:
        pass  # module doesn't exist, deal with it.
    # Ask user for project directory
    directory = input('Please enter your project directory:\n')
    # Ask user if they want to create basic desired directories
    basicDirectory = input('Do you want to create the desired directories? [y/n/info]\n')
    if basicDirectory == "y":
        print(
            "Please confirm your options:\n\nProject directory: " + directory + "\nPackages to install:\n\nelectron\ndotenv\n\nCreating the following directories/files:\napp/main/scripts/logging\napp/loading/img\n.gitconfig\n.gitignore\n.env\nindex.js\nindex.html (main)\nscript.js (main)\nstyle.css (main)\nlogging.js\nindex.html (loading)\nstyle.css (loading)")
        accept = input("Do you accept these changes? [y/n]\n")
        if accept == "y":
            # Change directory to user desired directory
            os.chdir(directory)
            time.sleep(2)

            # Install both dotenv and electron node modules
            os.system('npm install --save-dev electron')
            os.system('npm install dotenv')
            time.sleep(2)
            desired_directories()
        else:
            electron()
    elif basicDirectory == "n":
        print(
            "Please confirm your options:\n\nProject directory: " + directory + "\nPackages to install:\n\nelectron\ndotenv\n\nWon't create any other files")
        accept = input("Do you accept these changes? [y/n]\n")
        if accept == "y":
            # Change directory to user desired directory
            os.chdir(directory)
            time.sleep(2)

            # Install both dotenv and electron node modules
            os.system('npm install --save-dev electron')
            os.system('npm install dotenv')
            time.sleep(2)
            not_desired()
        else:
            electron()
    elif basicDirectory == "info":
        print(
            "The following packages/files will be installed when running this script.\n\nPackages to install:\n\nelectron\ndotenv\n\nCreating the following directories/files (These will NOT be installed if you select 'n'):\napp/main/scripts/logging\napp/loading/img\n.gitconfig\n.gitignore\n.env\nindex.js\nindex.html (main)\nscript.js (main)\nstyle.css (main)\nlogging.js\nindex.html (loading)\nstyle.css (loading)")
        electron()
    else:
        print("That was not an option please try again!")
        electron()

    def desired_directories():
        print('Start creating desired directories')
        if platform == "linux" or platform == "linux1" or platform == "linux2" or platform == "darwin":
            # Creating folders
            os.system('mkdir app')
            print('created app folder')
            os.system('mkdir app/main')
            print('created main folder')
            os.system('mkdir app/main/scripts')
            print('created scripts folder')
            os.system('mkdir app/main/scripts/logging')
            print('created logging folder')
            os.system('mkdir app/loading')
            print('created loading folder')
            os.system('mkdir app/loading/img')
            print('created img folder')
        elif platform == "win32":
            # Creating folders
            os.system('mkdir app')
            print('created app folder')
            os.system('mkdir app\\main')
            print('created main folder')
            os.system('mkdir app\\main\\scripts')
            print('created scripts folder')
            os.system('mkdir app\\main\\scripts\\logging')
            print('created logging folder')
            os.system('mkdir app\\loading')
            print('created loading folder')
            os.system('mkdir app\\loading\\img')
            print('created img folder')
        else:
            print('Your operating system is not supported')

        # Creating files with content
        with open('index.js', "w") as f:
            f.write(index_js)
            print('created index.js')
        with open(r'.env', 'w') as fp:
            fp.write('API_KEY =')
            print('created .env file')
            pass

        with open(r'.gitconfig', 'w') as fp:
            fp.write(gitconfig)
            print('created .gitconfig file')
            pass

        with open(r'.gitignore', 'w') as fp:
            fp.write(gitignore)
            print('created .gitignore file')
            pass

        with open(r'app/main/scripts/logging/logging.js', 'w') as fp:
            fp.write(logging_js)
            print('created logging.js file in app/main/scripts/logging/logging.js')
            pass

        with open(r'app/main/scripts/script.js', 'w') as fp:
            fp.write('')
            print('created script.js file in app/main/scripts/script.js')
            pass

        with open(r'app/main/index.html', 'w') as fp:
            fp.write(main_index_html)
            print('created index.js file in app/main/index.html')
            pass

        with open(r'app/main/style.css', 'w') as fp:
            fp.write('')
            print('created style.css file in app/main/style.css')
            pass

        with open(r'app/loading/index.html', 'w') as fp:
            fp.write(loading_index_html)
            print('created index.html file in app/loading/index.html')
            pass

        with open(r'app/loading/style.css', 'w') as fp:
            fp.write(loading_style_css)
            print('created index.html file in app/loading/style.css')
            pass

        # Get current time and
        currentTime = datetime.now().strftime("%H:%M:%S")
        print(
            'finished creating desired directories, happy coding!\n\nFinished at: ' + currentTime + '\nTotal duration: ' + "%s seconds" % (
                        time.time() - start_time))

    def not_desired():
        print('Did not create desired directories')
        # Get current time and
        currentTime = datetime.now().strftime("%H:%M:%S")
        print(
            'finished creating desired directories, happy coding!\n\nFinished at: ' + currentTime + '\nTotal duration: ' + "%s seconds" % (
                        time.time() - start_time))


# ----------------------------
# -                          -
# -           Yii            -
# -                          -
# ----------------------------

def Yii():
    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("Yii")
        print(ascii_banner)
    except ImportError as e:
        pass  # module doesn't exist, deal with it.
    # Giving the user options
    directory = input('Please enter your project directory:\n')
    projectName = input('Please enter the desired project name: ')
    databaseName = input('Please enter your database name (optional): ')
    print(
        "Please verify these changes: \n\nInstallation directory: " + directory + "\nProject name: " + projectName + "\nDatabase name: " + databaseName + "\n\n")
    acceptChanges = input("Do you accept these changes? [y/n]")

    if acceptChanges == 'y':
        print("Starting the download of Yii in the desired directory")

        db_config = """<?php

        return [
            'class' => 'yii\db\Connection',
            'dsn' => 'mysql:host=localhost;dbname=""" + projectName + """',
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
            'dsn' => 'mysql:host=localhost;dbname=""" + databaseName + """',
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
            os.chdir(directory + "/" + projectName)
            time.sleep(1)
            # Changing neccesary files
            with open(r'config/db.php', "w") as f:
                f.write(db_config)
                print('Changed the db.php file in the ' + projectName + '/config/db.php')

            with open(r'config/web.php', "w") as f:
                f.write(web_php)
                print('Changed the db.php file in the ' + projectName + '/config/web.php')
        else:
            # Change directory to user desired directory
            os.chdir(directory)
            time.sleep(2)

            # install section
            os.system('composer create-project --prefer-dist yiisoft/yii2-app-basic ' + projectName)

            print("Using database name for as database name")
            os.chdir(directory + "/" + projectName)
            time.sleep(1)
            # Changing neccesary files
            with open(r'config/db.php', "w") as f:
                f.write(db_config_dbname)
                print('Changed the db.php file in the ' + projectName + '/config/db.php')

            with open(r'config/web.php', "w") as f:
                f.write(web_php)
                print('Changed the db.php file in the ' + projectName + '/config/web.php')

        # Get current time and
        currentTime = datetime.now().strftime("%H:%M:%S")
        print(
            'finished creating desired directories, happy coding!\n\nFinished at: ' + currentTime + '\nTotal duration: ' + "%s seconds" % (
                        time.time() - start_time) + "\n\nStart Yii with the command: php yii serve")

    elif acceptChanges == 'n':
        exit()
    else:
        Yii()


# ----------------------------
# -                          -
# -      LARAVEL (CRUD)      -
# -                          -
# ----------------------------

def install_laravel(project_name, install_dir, db_name, db_user, db_password):
    if platform.system() == 'Windows':
        cmd = ['cmd', '/c', 'composer', 'create-project', '--prefer-dist', 'laravel/laravel:^10.0',
               os.path.join(install_dir, project_name)]
    else:
        cmd = ['composer', 'create-project', '--prefer-dist', 'laravel/laravel:^10.0',
               os.path.join(install_dir, project_name)]
    subprocess.run(cmd)
    os.chdir(os.path.join(install_dir, project_name))

    # Update composer.json to require PHP ^8.0 and illuminate/validation ^8.42
    with open('composer.json', 'r+') as f:
        composer_json = json.load(f)
        composer_json['require']['php'] = '*'
        composer_json['require']['illuminate/validation'] = '*'
        composer_json['require']['laravel/ui'] = '*'
        composer_json['require']['livewire/livewire'] = '*'
        f.seek(0)
        json.dump(composer_json, f, indent=4)
        f.truncate()

    # Copy .env.example to .env
    shutil.copy('.env.example', '.env')

    # Replace DB_DATABASE, DB_USERNAME, and DB_PASSWORD values in .env file
    with open('.env', 'r') as f:
        env_lines = f.readlines()

    with open('.env', 'w') as f:
        for line in env_lines:
            if line.startswith('DB_DATABASE='):
                line = 'DB_DATABASE={}\n'.format(db_name)
            elif line.startswith('DB_USERNAME='):
                line = 'DB_USERNAME={}\n'.format(db_user)
            elif line.startswith('DB_PASSWORD='):
                line = 'DB_PASSWORD={}\n'.format(db_password)
            f.write(line)

    # Run artisan key:generate command
    subprocess.run(['php', 'artisan', 'key:generate'])


def get_fields(table_name, db_user, db_password, db_name):
    # Replace with your own database configuration
    db = MySQLdb.connect(host="localhost", user=db_user, passwd=db_password, db=db_name)
    cursor = db.cursor()

    # Get column names for table
    cursor.execute("SHOW COLUMNS FROM " + table_name)
    fields = cursor.fetchall()

    # Return list of field names
    return [field[0] for field in fields]


def get_fieldsLINUX(table_name, db_user, db_password, db_name):
    # Replace with your own database configuration
    db = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()

    # Get column names for table
    cursor.execute("SHOW COLUMNS FROM " + table_name)
    fields = cursor.fetchall()

    # Return list of field names
    return [field[0] for field in fields]


def generate_crud(project_name, install_dir, sql_file_path, model_namespace, db_user, db_password, db_name):
    if platform.system() == 'Windows':
        # Read SQL file contents
        os.chdir(os.path.join(install_dir, project_name))
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_file_contents = f.read()

        # Extract table names from SQL file contents
        table_names = re.findall(r'CREATE TABLE `([a-zA-Z0-9_]+)`', sql_file_contents)

        # Generate migration, model, controller, and view files for each table
        for table_name in table_names:
            migration_name = f"create_{table_name}_table"
            model_name = f"{model_namespace}\\{table_name.title()}"

            # Check if table already exists
            output = subprocess.run(
                ["mysql.exe", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e", "SHOW TABLES"],
                capture_output=True, text=True)
            tables = output.stdout.splitlines()
            if table_name in tables:
                print(f"Table {table_name} already exists, skipping migration...")
                continue

            # Generate migration file
            subprocess.run(["php.exe", "artisan", "make:migration", migration_name, "--create=" + table_name])

            # Generate model and controller files
            subprocess.run(["php.exe", "artisan", "make:model", model_name, "--migration"])
            subprocess.run(["php.exe", "artisan", "migrate"])
            subprocess.run(["php.exe", "artisan", "migrate:refresh"])
            subprocess.run(["php.exe", "artisan", "make:controller", model_name + "Controller", "--resource",
                            "--model=" + model_name])
            subprocess.run(["php.exe", "artisan", "make:request", table_name.title() + "Request"])
            subprocess.run(["php.exe", "artisan", "key:generate"])

            # Generate view files for each table
            os.makedirs(os.path.join('resources', 'views', table_name.lower()), exist_ok=True)
            with open(os.path.join('resources', 'views', table_name.lower(), 'create.blade.php'), 'w') as f:
                f.write(
                    '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <form method="POST" action="{{ route(\'' + table_name.lower() + '.store\') }}">\n        @csrf\n')
                desc_output = subprocess.run(
                    ["mysql.exe", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e",
                     f"desc {table_name}"], capture_output=True, text=True)
                fields = desc_output.stdout.splitlines()
                for field in fields:
                    if field.split()[0] == "id":
                        continue
                    f.write(
                        f'        <div class="form-group">\n            <label for="{field.split()[0]}">{field.split()[0]}</label>\n            <input type="text" name="{field.split()[0]}" class="form-control" id="{field.split()[0]}" placeholder="{field.split()[0]}">\n        </div>\n')
                f.write(
                    f'        <button type="submit" class="btn btn-primary">Submit</button>\n    </form>\n@endsection\n')
            with open(os.path.join('resources', 'views', table_name.lower(), 'edit.blade.php'), 'w') as f:
                f.write(
                    '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <form method="POST" action="{{ route(\'' + table_name.lower() + '.update\', [${table_name.lower().rstrip("s")}->{table_name}_id]) }}">\n        @csrf\n        @method(\'PUT\')\n')
                desc_output = subprocess.run(
                    ["mysql.exe", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e",
                     f"desc {table_name}"], capture_output=True, text=True)
                fields = desc_output.stdout.splitlines()
                for field in fields:
                    if field.split()[0] == "id":
                        continue
                    f.write(
                        f'        <div class="form-group">\n            <label for="{field.split()[0]}">{field.split()[0]}</label>\n            <input type="text" name="{field.split()[0]}" value="{{ ${table_name.lower().rstrip("s")}->{field.split()[0]} }}" class="form-control" id="{field.split()[0]}" placeholder="{field.split()[0]}">\n        </div>\n')
                f.write(
                    f'        <button type="submit" class="btn btn-primary">Update</button>\n    </form>\n@endsection\n')
            with open(os.path.join('resources', 'views', table_name.lower(), 'show.blade.php'), 'w') as f:
                f.write(
                    '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <table class="table">\n')
                desc_output = subprocess.run(
                    ["mysql.exe", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e",
                     f"desc {table_name}"], capture_output=True, text=True)
            with open(os.path.join('resources', 'views', table_name.lower(), 'index.blade.php'), 'w') as f:
                f.write(
                    '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>index</h1>\n    <table class="table">\n')
                desc_output = subprocess.run(
                    ["mysql.exe", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e",
                     f"desc {table_name}"], capture_output=True, text=True)
            # Generate resource routes for each table
            with open(os.path.join('routes', 'web.php'), 'a') as f:
                f.write(
                    f"\nRoute::get('{table_name.lower()}', [App\Http\Controllers\{model_name.title()}Controller::class, 'index']);\n")

            # Generate controller file name based on table name
            controller_name = table_name.title() + "Controller"
            controller_file_name = controller_name + ".php"

            # Generate controller file contents
            controller_contents = "<?php\n\nnamespace App\Http\Controllers;\n\nuse Illuminate\Http\Request;\nuse App\\Models\\" + model_namespace + "\\" + table_name.title() + ";\n\nclass " + controller_name + " extends Controller\n{\n"

            # Generate index function
            controller_contents += "    public function index()\n    {\n        $" + table_name + " = " + table_name.title() + "::all();\n        return view('" + table_name + ".index', compact('" + table_name + "'));\n    }\n\n"

            # Generate create function
            controller_contents += "    public function create()\n    {\n        return view('" + table_name + ".create');\n    }\n\n"

            # Generate store function
            controller_contents += "    public function store(Request $request)\n    {\n        $request->validate([\n"
            # Add validation rules for each field
            for field in get_fields(table_name, db_user, db_password, db_name):
                controller_contents += "            '" + field + "' => 'required',\n"
            controller_contents += "        ]);\n\n        " + table_name.title() + "::create($request->all());\n\n        return redirect()->route('" + table_name + ".index')\n            ->with('success', '" + table_name.title() + " created successfully.');\n    }\n\n"

            # Generate show function
            controller_contents += "    public function show($" + table_name + ")\n    {\n        return view('" + table_name + ".show', compact('" + table_name + "'));\n    }\n\n"

            # Generate edit function
            controller_contents += "    public function edit($" + table_name + ")\n    {\n        return view('" + table_name + ".edit', compact('" + table_name + "'));\n    }\n\n"

            # Generate update function
            controller_contents += "    public function update(Request $request, $" + table_name + ")\n    {\n        $request->validate([\n"
            # Add validation rules for each field
            for field in get_fields(table_name, db_user, db_password, db_name):
                controller_contents += "            '" + field + "' => 'required',\n"
            controller_contents += "        ]);\n\n        $" + table_name + "->update($request->all());\n\n        return redirect()->route('" + table_name + ".index')\n            ->with('success', '" + table_name.title() + " updated successfully.');\n    }\n\n"

            # Generate destroy function
            controller_contents += "    public function destroy($" + table_name + ")\n    {\n        $" + table_name + "->delete();\n\n        return redirect()->route('" + table_name + ".index')\n            ->with('success', '" + table_name.title() + " deleted successfully.');\n    }\n}\n"

            # Write controller file to disk
            with open(os.path.join("app/Http/Controllers", controller_file_name), "w", encoding="utf-8") as f:
                f.write(controller_contents)

    # Determine path separator based on current OS
    path_separator = os.path.sep

    # Define path to base.blade.php file
    base_blade_path = os.path.join("resources", "views", "layouts", "base.blade.php")

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(base_blade_path), exist_ok=True)

    # Create base.blade.php file if it doesn't exist
    if not os.path.exists(base_blade_path):
        with open(base_blade_path, "w") as f:
            f.write(
                "<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head>\n"
                "    <meta charset=\"UTF-8\">\n"
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
                "    <meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">\n"
                "    <title>@yield('title')</title>\n"
                "</head>\n"
                "<body>\n"
                "    @yield('content')\n"
                "</body>\n"
                "</html>\n"
            )


def generate_crudLINUX(project_name, install_dir, sql_file_path, model_namespace, db_user, db_password, db_name):
    # Read SQL file contents
    os.chdir(os.path.join(install_dir, project_name))
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_file_contents = f.read()

    # Extract table names from SQL file contents
    table_names = re.findall(r'CREATE TABLE `([a-zA-Z0-9_]+)`', sql_file_contents)

    # Generate migration, model, controller, and view files for each table
    for table_name in table_names:
        migration_name = f"create_{table_name}_table"
        model_name = f"{model_namespace}/{table_name.title()}"

        # Generate migration file
        os.system(f"php artisan make:migration {migration_name} --create={table_name}")

        # Generate model and controller files
        os.system(f"php artisan make:model {model_name} --migration")
        os.system(f"php artisan migrate")
        os.system(f"php artisan migrate:refresh")
        os.system(f"php artisan make:controller {model_name}Controller --resource --model={model_name}")
        os.system(f"php artisan make:request {table_name.title()}Request")
        os.system(f"php artisan key:generate")

        # Generate view files for each table
        os.makedirs(os.path.join('resources', 'views', table_name.lower()), exist_ok=True)
        with open(os.path.join('resources', 'views', table_name.lower(), 'create.blade.php'), 'w') as f:
            f.write(
                '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <form method="POST" action="{{ route(\'' + table_name.lower() + '.store\') }}">\n        @csrf\n')
            desc_output = subprocess.run(
                ["mysql", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e", f"desc {table_name}"],
                capture_output=True, text=True)
            fields = desc_output.stdout.splitlines()
            for field in fields:
                if field.split()[0] == "id":
                    continue
                f.write(
                    f'        <div class="form-group">\n            <label for="{field.split()[0]}">{field.split()[0]}</label>\n            <input type="text" name="{field.split()[0]}" class="form-control" id="{field.split()[0]}" placeholder="{field.split()[0]}">\n        </div>\n')
            f.write(
                f'        <button type="submit" class="btn btn-primary">Submit</button>\n    </form>\n@endsection\n')
        with open(os.path.join('resources', 'views', table_name.lower(), 'edit.blade.php'), 'w') as f:
            f.write(
                '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <form method="POST" action="{{ route(\'' + table_name.lower() + '.update\', [${table_name.lower().rstrip("s")}->{table_name}_id]) }}">\n        @csrf\n        @method(\'PUT\')\n')
            desc_output = subprocess.run(
                ["mysql", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e", f"desc {table_name}"],
                capture_output=True, text=True)
            fields = desc_output.stdout.splitlines()
            for field in fields:
                if field.split()[0] == "id":
                    continue
                f.write(
                    f'        <div class="form-group">\n            <label for="{field.split()[0]}">{field.split()[0]}</label>\n            <input type="text" name="{field.split()[0]}" value="{{ ${table_name.lower().rstrip("s")}->{field.split()[0]} }}" class="form-control" id="{field.split()[0]}" placeholder="{field.split()[0]}">\n        </div>\n')
            f.write(
                f'        <button type="submit" class="btn btn-primary">Update</button>\n    </form>\n@endsection\n')
        with open(os.path.join('resources', 'views', table_name.lower(), 'show.blade.php'), 'w') as f:
            f.write(
                '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <table class="table">\n')
            desc_output = subprocess.run(
                ["mysql", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e", f"desc {table_name}"],
                capture_output=True, text=True)
        with open(os.path.join('resources', 'views', table_name.lower(), 'index.blade.php'), 'w') as f:
            f.write(
                '@extends(\'layouts.base\')\n\n@section(\'content\')\n    <h1>index</h1>\n    <table class="table">\n')
            desc_output = subprocess.run(
                ["mysql", "-u", db_user, "-p" + db_password, "-D", db_name, "-s", "-N", "-e", f"desc {table_name}"],
                capture_output=True, text=True)
        # Generate resource routes for each table
        with open(os.path.join('routes', 'web.php'), 'a') as f:
            f.write(
                f"\nRoute::get('{table_name.lower()}', [App\Http\Controllers\{table_name.title()}Controller::class, 'index']);\n")

            # Generate controller file name based on table name
            controller_name = table_name.title() + "Controller"
            controller_file_name = controller_name + ".php"

            # Generate controller file contents
            controller_contents = "<?php\n\nnamespace App\Http\Controllers;\n\nuse Illuminate\Http\Request;\nuse App\\Models\\" + model_namespace + "\\" + table_name.title() + ";\n\nclass " + controller_name + " extends Controller\n{\n"

            # Generate index function
            controller_contents += "    public function index()\n    {\n        $" + table_name + " = " + table_name.title() + "::all();\n        return view('" + table_name + ".index', compact('" + table_name + "'));\n    }\n\n"

            # Generate create function
            controller_contents += "    public function create()\n    {\n        return view('" + table_name + ".create');\n    }\n\n"

            # Generate store function
            controller_contents += "    public function store(Request $request)\n    {\n        $request->validate([\n"
            # Add validation rules for each field
            for field in get_fieldsLINUX(table_name, db_user, db_password, db_name):
                controller_contents += "            '" + field + "' => 'required',\n"
            controller_contents += "        ]);\n\n        " + table_name.title() + "::create($request->all());\n\n        return redirect()->route('" + table_name + ".index')\n            ->with('success', '" + table_name.title() + " created successfully.');\n    }\n\n"

            # Generate show function
            controller_contents += "    public function show($" + table_name + ")\n    {\n        return view('" + table_name + ".show', compact('" + table_name + "'));\n    }\n\n"

            # Generate edit function
            controller_contents += "    public function edit($" + table_name + ")\n    {\n        return view('" + table_name + ".edit', compact('" + table_name + "'));\n    }\n\n"

            # Generate update function
            controller_contents += "    public function update(Request $request, $" + table_name + ")\n    {\n        $request->validate([\n"
            # Add validation rules for each field
            for field in get_fieldsLINUX(table_name, db_user, db_password, db_name):
                controller_contents += "            '" + field + "' => 'required',\n"
            controller_contents += "        ]);\n\n        $" + table_name + "->update($request->all());\n\n        return redirect()->route('" + table_name + ".index')\n            ->with('success', '" + table_name.title() + " updated successfully.');\n    }\n\n"

            # Generate destroy function
            controller_contents += "    public function destroy($" + table_name + ")\n    {\n        $" + table_name + "->delete();\n\n        return redirect()->route('" + table_name + ".index')\n            ->with('success', '" + table_name.title() + " deleted successfully.');\n    }\n}\n"

            # Write controller file to disk
            with open(os.path.join("app/Http/Controllers", controller_file_name), "w", encoding="utf-8") as f:
                f.write(controller_contents)

    # Determine path separator based on current OS
    path_separator = os.path.sep

    # Define path to base.blade.php file
    base_blade_path = os.path.join("resources", "views", "layouts", "base.blade.php")

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(base_blade_path), exist_ok=True)

    # Create base.blade.php file if it doesn't exist
    if not os.path.exists(base_blade_path):
        with open(base_blade_path, "w") as f:
            f.write(
                "<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head>\n"
                "    <meta charset=\"UTF-8\">\n"
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
                "    <meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">\n"
                "    <title>@yield('title')</title>\n"
                "</head>\n"
                "<body>\n"
                "    @yield('content')\n"
                "</body>\n"
                "</html>\n"
            )


def laravel():
    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("Laravel (CRUD)")
        print(ascii_banner)
        print("Host operating system: " + platform.system())
    except ImportError as e:
        pass  # module doesn't exist, deal with it.
    project_name = input('Enter the project name: ')
    install_dir = input('Enter the installation directory (default: current directory): ') or '.'
    db_name = input('Enter the database name: ')
    db_user = input('Enter the database username: ')
    db_password = input('Enter the database password: ')
    use_phpmyadmin = input('Do you want to use phpMyAdmin (y/n)? ').lower() == 'y'
    sql_file_path = input("Enter the path to the SQL file: ")
    model_namespace = input("Enter the model namespace: ")

    # Install Laravel and generate CRUD files
    if platform.system() == 'Windows':
        install_laravel(project_name, install_dir, db_name, db_user, db_password)
        generate_crud(project_name, install_dir, sql_file_path, model_namespace, db_user, db_password, db_name)
    elif platform.system() == 'Linux':
        install_laravel(project_name, install_dir, db_name, db_user, db_password)
        generate_crudLINUX(project_name, install_dir, sql_file_path, model_namespace, db_user, db_password, db_name)

    # Update composer.json and install required packages
    os.chdir(os.path.join(install_dir, project_name))
    with open('composer.json', 'r') as f:
        composer_data = json.load(f)
        composer_data['require']['laravel/ui'] = '*'
        with open('composer.json', 'w') as fw:
            json.dump(composer_data, fw, indent=4)
    subprocess.run(['composer', 'update'])

    # Run Laravel UI commands
    if use_phpmyadmin:
        subprocess.run(['php', 'artisan', 'ui', 'bootstrap'])
        subprocess.run(['php', 'artisan', 'ui', 'auth'])
        subprocess.run(['npm', 'install'])
        subprocess.run(['npm', 'run', 'dev'])

    # Serve Laravel
    subprocess.run(['php', 'artisan', 'serve'])


# ----------------------------
# -                          -
# -         LARAVEL          -
# -                          -
# ----------------------------

def install_laravel_only(project_name, install_dir, db_name, db_user, db_password):
    if platform.system() == 'Windows':
        cmd = ['cmd', '/c', 'composer', 'create-project', '--prefer-dist', 'laravel/laravel:^10.0',
               os.path.join(install_dir, project_name)]
    else:
        cmd = ['composer', 'create-project', '--prefer-dist', 'laravel/laravel:^10.0',
               os.path.join(install_dir, project_name)]
    subprocess.run(cmd)
    os.chdir(os.path.join(install_dir, project_name))

    # Update composer.json to require PHP ^8.0 and illuminate/validation ^8.42
    with open('composer.json', 'r+') as f:
        composer_json = json.load(f)
        composer_json['require']['php'] = '*'
        composer_json['require']['illuminate/validation'] = '*'
        composer_json['require']['laravel/ui'] = '*'
        composer_json['require']['livewire/livewire'] = '*'
        f.seek(0)
        json.dump(composer_json, f, indent=4)
        f.truncate()

    subprocess.run(['cp', '.env.example', '.env'])
    subprocess.run(['sed', '-i', 's/DB_DATABASE=.*/DB_DATABASE=' + db_name + '/', '.env'])
    subprocess.run(['sed', '-i', 's/DB_USERNAME=.*/DB_USERNAME=' + db_user + '/', '.env'])
    subprocess.run(['sed', '-i', 's/DB_PASSWORD=.*/DB_PASSWORD=' + db_password + '/', '.env'])


def laravel_only():
    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("Laravel")
        print(ascii_banner)
    except ImportError as e:
        pass  # module doesn't exist, deal with it.
    project_name = input('Enter the project name: ')
    install_dir = input('Enter the installation directory (default: current directory): ') or '.'
    db_name = input('Enter the database name: ')
    db_user = input('Enter the database username: ')
    db_password = input('Enter the database password: ')

    install_laravel_only(project_name, install_dir, db_name, db_user, db_password)


def main():
    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("Automation Scripts")
        print(ascii_banner)
    except ImportError as e:
        pass  # module doesn't exist, deal with it.

    choiceSelect = input(
        "Please select one of the following that you want to install:\n\n[1] Electron basic template\n[2] Yii2 install autiomation\n[3] Laravel (with crud generator)\n")

    if choiceSelect == '1':
        electron()
    elif choiceSelect == '2':
        Yii()
    elif choiceSelect == '3':
        laravelSelect = input(
            "How do you want to install laravel?\n\n[1] With CRUD generator\n[2] Without CRUD generator (blank install)\n\n[99] Back\n")
        if laravelSelect == '1':
            laravel()
        elif laravelSelect == '2':
            laravel_only()
        elif laravelSelect == '99':
            main()
        else:
            print("That was not an option, sending you back to the start.")
            time.sleep(2)
            main()
    else:
        print('Selected option does not exist, please try again')
        main()


main()