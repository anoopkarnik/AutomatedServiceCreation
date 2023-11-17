from flask import Flask
import threading
import os
import atexit
# from extensions import db
from main.controllers import Controller
from dotenv import load_dotenv
import logging

load_dotenv()

def create_app():
	app = Flask(__name__)
	logging.basicConfig(filename='logs/scheduler.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')
	# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
	# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	# db.init_app(app)
	app.logger.info('Info level log')
	app.logger.error('Error level log')
	app.register_blueprint(Controller.payload_controller)
	return app

app = create_app()

if __name__ == "__main__":
	# with app.app_context():
	# 	db.create_all()
	app.run(debug=True)