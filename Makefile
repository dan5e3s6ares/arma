run/tests:
	python -m unittest discover -s tests -p "test_*.py"

server/start:
	uvicorn main:app --reload

arma/start:
	docker compose up --build -d

coverage:
	coverage run -m unittest && coverage report -m