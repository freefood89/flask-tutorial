deps:
	pip install -r requirements.txt

test:
	pytest

tdd:
	ptw

install:
	pip install --user -e .

init:
	flask db init

migrate:
	flask db migrate 
	flask db upgrade

run:
	flask run -h 0.0.0.0

debug:
	FLASK_DEBUG=1 python3 run.py
