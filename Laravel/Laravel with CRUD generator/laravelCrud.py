import os
import subprocess
import json
import re
import platform
# ----------------------------
# -                          -
# -      LARAVEL (CRUD)      -
# -                          -
# ----------------------------


def install_laravel(project_name, install_dir, db_name, db_user, db_password):
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



def generate_crud(project_name, install_dir, sql_file_path, model_namespace, db_user, db_password, db_name):
    # Read SQL file contents
    os.chdir(os.path.join(install_dir, project_name))
    with open(sql_file_path, 'r') as f:
        sql_file_contents = f.read()

    # Extract table names from SQL file contents
    table_names = re.findall(r'CREATE TABLE `([a-zA-Z0-9_]+)`', sql_file_contents)

    # Generate migration, model, controller, and view files for each table
    for table_name in table_names:
        migration_name = f"create_{table_name}_table"
        model_name = f"{model_namespace}\\{table_name.title()}"

        # Generate migration file
        os.system(f"php artisan make:migration {migration_name} --create={table_name}")

        # Generate model and controller files
        os.system(f"php artisan make:model {model_name} --migration")
        os.system(f"php artisan make:controller {model_name}Controller --resource --model={model_name}")
        os.system(f"php artisan make:request {table_name.title()}Request")
        os.system(f"php artisan key:generate")

        # Generate view files
        os.makedirs(os.path.join('resources', 'views', table_name.lower()), exist_ok=True)
        with open(os.path.join('resources', 'views', table_name.lower(), 'index.blade.php'), 'w') as f:
            f.write('@extends(\'layouts.app\')\n\n@section(\'content\')\n    <h1>{{ $title }}</h1>\n    <table class="table">\n        <thead>\n            <tr>\n')
            with os.popen(f"mysql -u{db_user} -p{db_password} -D{db_name} -s -N -e \"desc {table_name};\"") as desc_output:
                fields = desc_output.readlines()
            for field in fields:
                f.write(f'                <th scope="col">{field.strip()}</th>\n')
            f.write('                <th scope="col">Actions</th>\n')
            f.write('            </tr>\n        </thead>\n        <tbody>\n')
            f.write(f'            @foreach (${table_name.lower()} as ${table_name.lower().rstrip("s")})\n')
            f.write(f'                <tr>\n')
            for field in fields:
                f.write(f'                    <td>{{ ${table_name.lower().rstrip("s")}->{field.split()[0]} }}</td>\n')
            f.write(f'                    <td><a href="{{ route(\'{table_name.lower()}.show\', [${table_name.lower().rstrip("s")}->{table_name}_id]) }}">Show</a> | <a href="{{ route(\'{table_name.lower()}.edit\', [${table_name.lower().rstrip("s")}->{table_name}_id]) }}">Edit</a> | <form action="{{ route(\'{table_name.lower()}.destroy\', [${table_name.lower().rstrip("s")}->{table_name}_id]) }}" method="POST">@csrf @method(\'DELETE\')<button type="submit" class="btn btn-link">Delete</button></form></td>\n')
            f.write(f'                </tr>\n            @endforeach\n')
            f.write('        </tbody>\n    </table>\n    <a href="{{ route(\'{table_name.lower()}.create\') }}" class="btn btn-primary">Create</a>\n')
            f.write('@endsection\n')

def laravel():
    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("Laravel (CRUD)")
        print(ascii_banner)
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
    install_laravel(project_name, install_dir, db_name, db_user, db_password)
    generate_crud(project_name, install_dir, sql_file_path, model_namespace, db_user, db_password, db_name)

    # Update composer.json and install required packages
    os.chdir(os.path.join(install_dir, project_name))
    with open('composer.json', 'r') as f:
        composer_data = json.load(f)
        composer_data['require']['laravel/ui'] = '^3.4'
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