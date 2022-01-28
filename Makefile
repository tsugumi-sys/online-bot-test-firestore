.PHONY: test
test:
	poetry run python sample.py

.PHONY: run
run:
	poetry run uvicorn app.main:app --reload --host=0.0.0.0 --port=8080
