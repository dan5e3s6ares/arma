run/tests:
	python -m unittest discover -s tests -p "test_*.py"

server/start:
	uvicorn main:app --reload