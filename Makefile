# Makefile
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv 
# 	python -m pytest -vv test_costs.py

format:
#	black *.py
	find . -name \*\.py |xargs black


lint:
	pylint --disable=R,C src
	pylint --disable=R,C tests
#	pylint --disable=R,C cov=costs costs.py

clean:
	find . -name '__pycache__' -exec rm -fr {} +

all: install lint test format clean