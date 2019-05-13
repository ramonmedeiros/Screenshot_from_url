default: run

run:
	PYTHONPATH=. FLASK_APP=service.py FLASK_ENV=development flask run

