from flask import Blueprint, request, jsonify

from ..services.create_service import create_service
from ..services.delete_service import delete_service

payload_controller = Blueprint("payload_controller",__name__)

@payload_controller.route("/",methods=["GET"])
def health_check():
	return jsonify({"status":"success"})

@payload_controller.route("/create_service",methods=["POST"])
def create_service_controller():
	data = request.json
	service_type = data.get('service_type')
	folder_path = data.get('folder_path')
	service_name = data.get('service_name')
	service_port = data.get('service_port')
	github_boolean = data.get('github_boolean')
	local_boolean = data.get('local_boolean')
	ecr_boolean = data.get('ecr_boolean')
	create_service(service_type,folder_path,service_name,github_boolean,local_boolean,ecr_boolean,service_port)
	return jsonify({'message':'Service created successfully'})

@payload_controller.route("/delete_service",methods=["POST"])
def delete_service_controller():
	data = request.json
	service_type = data.get('service_type')
	folder_path = data.get('folder_path')
	service_name = data.get('service_name')
	github_boolean = data.get('github_boolean')
	local_boolean = data.get('local_boolean')
	ecr_boolean = data.get('ecr_boolean')
	image_boolean = data.get('image_boolean')
	container_boolean = data.get('container_boolean')
	delete_service(service_type,folder_path,service_name,github_boolean,local_boolean,ecr_boolean,image_boolean,container_boolean)
	return jsonify({'message':'Service deleted successfully'})


