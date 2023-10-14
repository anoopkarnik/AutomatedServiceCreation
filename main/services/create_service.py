import os
import shutil

def create_service(service_type,folder_path,service_name,github_boolean):
    input_path = os.path.join(folder_path,service_name)

    if '/' in service_name:
        service_name = service_name.split('/')[-1]
    
    os.system("mkdir -p {}".format(input_path))
    os.system("cd {}".format(input_path))
    print(input_path)
    if service_type =="flask":
        os.system("cd {} && python3.8 -m venv python-local".format(input_path))
        os.system("cd {} && source python-local/bin/activate".format(input_path))
        os.system("cd {} && mkdir app".format(input_path))
        os.system("cd {}/app && mkdir main".format(input_path))
        os.system("cd {}/app/main && mkdir controllers".format(input_path))
        os.system("cd {}/app/main && mkdir models".format(input_path))
        os.system("cd {}/app/main && mkdir services".format(input_path))
        os.system("cd {}/app && mkdir test".format(input_path))
        parent_directory = os.getcwd()
        # parent_directory = os.path.dirname(current_directory)

        source_path = os.path.join(parent_directory,"main/commons",service_type)
        gitignore_path = os.path.join(source_path,'.gitignore')
        app_py_path = os.path.join(source_path,'app.py')
        env_path = os.path.join(source_path,'.env')
        dockerfile_path = os.path.join(source_path,'Dockerfile')
        controller_path = os.path.join(source_path,'Controller.py')
        model_path = os.path.join(source_path,'Model.py')
        readme_path = os.path.join(source_path,'README.md')
        requirements_path = os.path.join(source_path,'requirements.txt')

        shutil.copy(gitignore_path,os.path.join(input_path,'app'))
        shutil.copy(app_py_path,os.path.join(input_path,'app'))
        shutil.copy(env_path,os.path.join(input_path,'app'))
        shutil.copy(dockerfile_path,os.path.join(input_path,'app'))
        shutil.copy(controller_path,os.path.join(input_path,'app/main/controllers'))
        shutil.copy(model_path,os.path.join(input_path,'app/main/models'))
        shutil.copy(readme_path,os.path.join(input_path,'app'))
        shutil.copy(requirements_path,os.path.join(input_path,'app'))

        os.system('source {}/python-local/bin/activate && pip install -r requirements.txt')

        if github_boolean == True:
            os.system("cd {}/app && git init".format(input_path))
            os.system("cd {}/app && git add .".format(input_path))
            os.system('cd {}/app && git commit -m "first commit"'.format(input_path))
            os.system('cd {}/app && git branch -M main'.format(input_path))
            os.system('cd {}/app && gh create-repo {}'.format(input_path,service_name))
            os.system('cd {}/app && git remote add origin https://github.com/anoopkarnik/{}.git'.format(input_path,service_name))
            os.system('cd {}/app && git push -u origin main'.format(input_path))
