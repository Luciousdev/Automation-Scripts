import os
import subprocess
import platform
import json
# ----------------------------
# -                          -
# -         LARAVEL          -
# -                          -
# ----------------------------

def install_laravel_only(project_name, install_dir, db_name, db_user, db_password):
    if platform.system() == 'Windows':
        cmd = ['cmd', '/c', 'composer', 'create-project', '--prefer-dist', 'laravel/laravel:^8.0', os.path.join(install_dir, project_name)]
    else:
        cmd = ['composer', 'create-project', '--prefer-dist', 'laravel/laravel:^8.0', os.path.join(install_dir, project_name)]
    subprocess.run(cmd)
    os.chdir(os.path.join(install_dir, project_name))
    
    # Update composer.json to require PHP ^8.0 and illuminate/validation ^8.42
    with open('composer.json', 'r+') as f:
        composer_json = json.load(f)
        composer_json['require']['php'] = '^8.0'
        composer_json['require']['illuminate/validation'] = '^8.42'
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

laravel_only()