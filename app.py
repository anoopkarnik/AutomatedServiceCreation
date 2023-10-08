from flask import Flask
import threading
import os
from main.models.SampleModel import db
from main.controllers import SampleController
from config import LocalConfig,CloudConfig
def create_app():
	app = Flask(__name__)
	app.config["ENV"] = os.environ.get("APP_ENV", "local")
	if app.config["ENV"] =="local":
		app.config.from_object(LocalConfig)
	elif app.config["ENV"] =="cloud":
		app.config.from_object(CloudConfig)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+app.config['DB_USERNAME']+':'+app.config['DB_PASSWORD']+'@'+app.config['DB_HOST']+':'+app.config['DB_PORT']+'/'+app.config['DB_NAME']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.register_blueprint(SampleController.payload_controller)
	return app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
