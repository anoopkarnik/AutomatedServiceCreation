import os
import requests
import boto3

def delete_service(service_type, folder_path, service_name, github_boolean, local_boolean, ecr_boolean, image_boolean, container_boolean):
    input_path = os.path.join(folder_path, service_name)

    github_owner = os.environ.get('GITHUB_OWNER')
    github_token = os.environ.get('GITHUB_TOKEN')
    aws_access_key_id= os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    ipv4_dns = os.environ.get('IPV4_DNS')
    ec2_pem_key_path = os.environ.get('EC2_PEM_KEY_PATH')
    aws_account_no = os.environ.get('AWS_ACCOUNT_NO')
    
    if '/' in service_name:
        service_name = service_name.split('/')[-1]
        
    if local_boolean:
        # Delete local folder
        os.system(f"rm -rf {input_path}")

    if github_boolean:
        # Delete GitHub repo
        headers = {"Authorization": "Bearer {}".format(github_token), "Accept": "application/vnd.github+json", "X-Github-Api-Version": "2022-11-28"}
        requests.delete(f'https://api.github.com/repos/{github_owner}/{service_name}', headers=headers)
    
    if ecr_boolean:
        # Delete ECR repo
        ecr_client = boto3.client('ecr', region_name='ap-south-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        ecr_client.delete_repository(repositoryName=service_name, force=True)

    if container_boolean:
        os.system(f"ssh -o StrictHostKeyChecking=no -i {ec2_pem_key_path} ubuntu@{ipv4_dns} 'sudo docker rm --force {service_name}'")
   
        
    if image_boolean:
        os.system(f"ssh -o StrictHostKeyChecking=no -i {ec2_pem_key_path} ubuntu@{ipv4_dns} 'sudo docker rmi {aws_account_no}.dkr.ecr.ap-south-1.amazonaws.com/{service_name}'")
    


