from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

payload_controller = Blueprint("payload_controller",__name__)

@payload_controller.route("/",methods=["GET"])
def health_check():
	return jsonify({"status":"success"})