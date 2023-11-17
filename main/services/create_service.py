import os
import shutil
import requests
import json

def create_service(service_type,folder_path,service_name,github_boolean,local_boolean,ecr_boolean,service_port):
    input_path = os.path.join(folder_path,service_name)

    if '/' in service_name:
        service_name = service_name.split('/')[-1]
    
    os.system("mkdir -p {}".format(input_path))
    os.system("cd {}".format(input_path))
    print(input_path)
    if service_type =="flask":
        if local_boolean == True:
            os.system("cd {} && python3.8 -m venv python-local".format(input_path))
            os.system("cd {} && source python-local/bin/activate".format(input_path))
            os.system("cd {} && mkdir app".format(input_path))
            os.system("cd {}/app && mkdir main".format(input_path))
            os.system("cd {}/app && mkdir logs".format(input_path))
            os.system("cd {}/app/main && mkdir controllers".format(input_path))
            os.system("cd {}/app/main && mkdir models".format(input_path))
            os.system("cd {}/app/main && mkdir services".format(input_path))
            os.system("cd {}/app && mkdir test".format(input_path))
            os.system("cd {}/app && mkdir -p .github/workflows".format(input_path))
            parent_directory = os.getcwd()
            # parent_directory = os.path.dirname(current_directory)

            source_path = os.path.join(parent_directory,"main/commons",service_type)
            gitignore_path = os.path.join(source_path,'.gitignore')
            app_py_path = os.path.join(source_path,'app.py')
            env_path = os.path.join(source_path,'.env')
            dockerfile_path = os.path.join(source_path,'Dockerfile')
            extensions_path = os.path.join(source_path,'extensions.py')
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
            shutil.copy(extensions_path,os.path.join(input_path,'app'))
            
            with open(os.path.join(input_path,'app/Dockerfile'),'r') as f:
                contents = f.read()
            
            contents = contents.replace("{{port_no}}",service_port)

            with open(os.path.join(input_path,'app/Dockerfile'),'w') as f:
                f.write(contents)

            os.system('source {}/python-local/bin/activate && pip install -r requirements.txt')

        if github_boolean == True:
            create_github_repository(input_path,service_name)

        if ecr_boolean == True:
            create_ecr_repository(input_path,service_name,service_type)



def create_github_repository(input_path,service_name):
    os.system("cd {}/app && git init".format(input_path))
    os.system("cd {}/app && git add .".format(input_path))
    os.system('cd {}/app && git commit -m "first commit"'.format(input_path))
    os.system('cd {}/app && git branch -M main'.format(input_path))
    os.system('cd {}/app && gh create-repo {}'.format(input_path,service_name))
    os.system('cd {}/app && git remote add origin https://github.com/anoopkarnik/{}.git'.format(input_path,service_name))
    os.system('cd {}/app && git push -u origin main'.format(input_path))

    owner = os.environ.get('GITHUB_OWNER')
    token = os.environ.get('GITHUB_TOKEN')
    aws_access_key_id= os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    ipv4_dns = os.environ.get('IPV4_DNS')
    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    s3_key_file_name = os.environ.get('S3_KEY_FILE_NAME')

    token_id_url = "https://api.github.com/repos/{}/{}/actions/secrets/public-key".format(owner,service_name)
    headers = {"Authorization": "Bearer {}".format(token), "Accept": "application/vnd.github+json", "X-Github-Api-Version": "2022-11-28"}
    response = requests.get(token_id_url,headers=headers).json()
    print(response)
    key_id = response['key_id']

    url = "https://api.github.com/repos/{}/{}/actions/variables".format(owner,service_name)
    payload = {"name":"AWS_ACCESS_KEY_ID","value":aws_access_key_id}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

    payload = {"name":"AWS_SECRET_ACCESS_KEY","value":aws_secret_access_key}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

    payload = {"name":"ECR_REPOSITORY","value":service_name}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

    payload = {"name":"IPV4_DNS","value":ipv4_dns}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

    payload = {"name":"S3_BUCKET_NAME","value":s3_bucket_name}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

    payload = {"name":"S3_KEY_FILE_NAME","value":s3_key_file_name}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

def create_ecr_repository(input_path,service_name,service_type):
    parent_directory = os.getcwd()
    commons_path = os.path.join(parent_directory,"main/commons",service_type)
    create_push_ecr_path = os.path.join(commons_path,'create_push_ecr.yml')
    shutil.copy(create_push_ecr_path,os.path.join(input_path,'app/.github/workflows'))
    os.system("cd {}/app && git add .".format(input_path))
    os.system('cd {}/app && git commit -m "added push to ecr workflow"'.format(input_path))
    os.system('cd {}/app && git push -u origin main'.format(input_path))


