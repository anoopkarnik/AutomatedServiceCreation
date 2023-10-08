from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SampleModel(db.Model):
	__tablename__ = ""
	__table_args__ = {"schema":""}
	id = db.Column(db.Integer, primary_key=True)
