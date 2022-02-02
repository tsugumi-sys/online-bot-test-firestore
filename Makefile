.PHONY: test
test:
	poetry run python -m unittest -v

.PHONY: run
run:
	poetry run uvicorn app.main:app --reload --host=0.0.0.0 --port=8080
