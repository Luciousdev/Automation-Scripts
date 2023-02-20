# Import mudules
import os
import time
from datetime import datetime
import time
from sys import platform
start_time = time.time()


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

gitignore ="""
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

def main():
    # Ask user for project directory
    directory = input('Please enter your project directory:\n')
    # Ask user if they want to create basic desired directories
    basicDirectory = input('Do you want to create the desired directories? [y/n/info]\n')
    if basicDirectory == "y":
        print("Please confirm your options:\n\nProject directory: " + directory + "\nPackages to install:\n\nelectron\ndotenv\n\nCreating the following directories/files:\napp/main/scripts/logging\napp/loading/img\n.gitconfig\n.gitignore\n.env\nindex.js\nindex.html (main)\nscript.js (main)\nstyle.css (main)\nlogging.js\nindex.html (loading)\nstyle.css (loading)")
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
            main()
    elif basicDirectory == "n":
        print("Please confirm your options:\n\nProject directory: " + directory + "\nPackages to install:\n\nelectron\ndotenv\n\nWon't create any other files")
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
            main()
    elif basicDirectory == "info":
        print("The following packages/files will be installed when running this script.\n\nPackages to install:\n\nelectron\ndotenv\n\nCreating the following directories/files (These will NOT be installed if you select 'n'):\napp/main/scripts/logging\napp/loading/img\n.gitconfig\n.gitignore\n.env\nindex.js\nindex.html (main)\nscript.js (main)\nstyle.css (main)\nlogging.js\nindex.html (loading)\nstyle.css (loading)")
        main()
    else:
        print("That was not an option please try again!")
        main()




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
    print('finished creating desired directories, happy coding!\n\nFinished at: ' + currentTime + '\nTotal duration: ' + "%s seconds" % (time.time() - start_time))


def not_desired():
    print('Did not create desired directories') 
    # Get current time and 
    currentTime = datetime.now().strftime("%H:%M:%S")
    print('finished creating desired directories, happy coding!\n\nFinished at: ' + currentTime + '\nTotal duration: ' + "%s seconds" % (time.time() - start_time))


main()