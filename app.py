from flask import Flask
import threading
import os
from main.controllers import Controller
from dotenv import load_dotenv
load_dotenv()

def create_app():
	app = Flask(__name__)
	app.register_blueprint(Controller.payload_controller)
	return app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
