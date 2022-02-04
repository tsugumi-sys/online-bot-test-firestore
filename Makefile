.PHONY: test
test:
	poetry run python -m unittest -v

IMAGE_URL=gcr.io/online-bot-test-logging/online-bot-test:latest
.PHONY: build
build:
	docker build . --tag $(IMAGE_URL)

.PHONY: push
push:
	docker push $(IMAGE_URL)

.PHONY: run
run:
	poetry run uvicorn app.main:app --reload --host=0.0.0.0 --port=8080
