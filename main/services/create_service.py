import os
import shutil
import requests
import json
import boto3

def create_service(service_type,folder_path,service_name,github_boolean,local_boolean,ecr_boolean,s3_boolean,
                   service_port,website_name):
    input_path = os.path.join(folder_path,service_name)

    if '/' in service_name:
        service_name = service_name.split('/')[-1]
    print(input_path)
    if service_type =="flask":
        if local_boolean == True:
            os.system("mkdir -p {}".format(input_path))
            os.system("cd {}".format(input_path))
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
            create_flask_github_repository(input_path,service_name)

        if ecr_boolean == True:
            create_ecr_repository(input_path,service_name,service_type)

    elif service_type=='react':
        if local_boolean == True:
            os.system("cd {} && npm create vite@latest {} -- --template react".format(folder_path,service_name))
            os.system("cd {} && npm install -D tailwindcss postcss autoprefixer".format(input_path))
            os.system("cd {} && npx tailwindcss init -p".format(input_path))
            os.system("cd {} && mkdir -p .github/workflows".format(input_path))
            os.system("cd {} && npm i react-router-dom".format(input_path))
            os.system("cd {} && npm i framer-motion".format(input_path))
            parent_directory = os.getcwd()

            source_path = os.path.join(parent_directory,"main/commons",service_type)
            print(source_path)
            tailwind_config_path = os.path.join(source_path,'tailwind.config.js')
            index_path = os.path.join(source_path,'index.css')
            env_path = os.path.join(source_path,'.env')
            dockerfile_path = os.path.join(source_path,'Dockerfile')
            app_path = os.path.join(source_path,'App.jsx')
            readme_path = os.path.join(source_path,'README.md')

            shutil.copy(tailwind_config_path, input_path)
            shutil.copy(index_path,os.path.join(input_path,'src'))
            shutil.copy(env_path,input_path)
            shutil.copy(dockerfile_path,input_path)
            shutil.copy(app_path,os.path.join(input_path,'src'))
            shutil.copy(readme_path,input_path)
        if github_boolean == True:
            create_react_github_repository(input_path,service_name,website_name)

        if s3_boolean == True:
            push_to_s3(input_path,service_name,service_type,website_name)


def create_flask_github_repository(input_path,service_name):
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


def create_react_github_repository(input_path,service_name,website_name):
    os.system("cd {} && git init".format(input_path))
    os.system("cd {} && git add .".format(input_path))
    os.system('cd {} && git commit -m "first commit"'.format(input_path))
    os.system('cd {}/ && git branch -M main'.format(input_path))
    os.system('cd {} && gh create-repo {}'.format(input_path,service_name))
    os.system('cd {} && git remote add origin https://github.com/anoopkarnik/{}.git'.format(input_path,service_name))
    os.system('cd {} && git push -u origin main'.format(input_path))

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

    payload = {"name":"WEBSITE_NAME","value":website_name}
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print(response)

def create_ecr_repository(input_path,service_name,service_type):
    parent_directory = os.getcwd()
    commons_path = os.path.join(parent_directory,"main/commons",service_type)
    create_push_ecr_path = os.path.join(commons_path,'create_push_ecr_and_deploy_image_to_ec2.yml')
    shutil.copy(create_push_ecr_path,os.path.join(input_path,'app/.github/workflows'))
    os.system("cd {}/app && git add .".format(input_path))
    os.system('cd {}/app && git commit -m "added push to ecr workflow"'.format(input_path))
    os.system('cd {}/app && git push -u origin main'.format(input_path))

def create_s3_static_website(bucket_name, region='ap-south-1'):
    # Create an S3 client
    region = os.environ.get('AWS_REGION')
    s3 = boto3.client('s3', region_name=region,
                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    # Create the S3 bucket
    if region == 'us-east-1':  # 'us-east-1' has a different syntax
        s3.create_bucket(Bucket=bucket_name)
        s3.create_bucket(Bucket="www."+bucket_name)
    else:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        s3.create_bucket(Bucket="www."+bucket_name, CreateBucketConfiguration={'LocationConstraint': region})

    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )
    s3.put_public_access_block(
        Bucket="www."+bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )
    # Set the website configuration
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }

    s3.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_configuration)
    website_configuration = {
        'RedirectAllRequestsTo': {
            'HostName': bucket_name,
            'Protocol': 'http'
        }
    }
    s3.put_bucket_website(Bucket="www."+bucket_name, WebsiteConfiguration=website_configuration)

    # Set the bucket policy to make the content publicly readable
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }]
    }
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::www.{bucket_name}/*"]
        }]
    }
    s3.put_bucket_policy(Bucket="www."+bucket_name, Policy=json.dumps(policy))
    
    # Return the website URL
    website_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
    return website_url

def push_to_s3(input_path,service_name,service_type,website_name):
    parent_directory = os.getcwd()
    commons_path = os.path.join(parent_directory,"main/commons",service_type)
    create_push_s3_path = os.path.join(commons_path,'deploy_to_s3.yml')
    bucket_name = create_s3_static_website(website_name)
    print(bucket_name)
    shutil.copy(create_push_s3_path,os.path.join(input_path,'.github/workflows'))
    os.system("cd {} && git add .".format(input_path))
    os.system('cd {} && git commit -m "added deploy to s3 workflow"'.format(input_path))
    os.system('cd {} && git push -u origin main'.format(input_path))


