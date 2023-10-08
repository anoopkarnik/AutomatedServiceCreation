import os

class Config:
	DEBUG = False

class LocalConfig:
	DEBUG = True
	DB_USERNAME = ""
	DB_PASSWORD = ""
	DB_HOST = ""
	DB_NAME = ""
	DB_PORT= ""

class CloudConfig:
	DEBUG = True
	DB_USERNAME = ""
	DB_PASSWORD = ""
	DB_HOST = ""
	DB_NAME = ""
	DB_PORT= ""
