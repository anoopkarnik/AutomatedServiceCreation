from flask import Blueprint, request, jsonify

from ..services.create_service import create_service

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
	github_boolean = data.get('github_boolean')
	create_service(service_type,folder_path,service_name,github_boolean)
	return jsonify({'message':'Service created successfully'})

