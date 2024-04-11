install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_costs.py

format:
	black *.py


lint:
	pylint --disable=R,C costs.py
#	pylint --disable=R,C cov=costs costs.py

all: install format lint test