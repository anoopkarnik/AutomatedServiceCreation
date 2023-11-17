#To run this app

flask run

or

gunicorn -w 1 -b 0.0.0.0:8111 --access-logfile logs/access.log --error-logfile logs/error.log app:app