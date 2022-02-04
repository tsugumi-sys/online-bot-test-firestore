.PHONY: test
test:
	poetry run python -m unittest -v


.PHONY: run
run:
	poetry run uvicorn app.main:app --reload --host=0.0.0.0 --port=8080

generate_openapi_json:
	poetry run python generate_openapi_schema.py


PROJECT_NAME=online-bot-test-logging
ARTIFACT_REGISTORY_REPOSITORY_NAME=online-bot-test-backend
IMAGE_NAME_WITH_TAG=online-bot-test-backend-image:latest
IMAGE_URL=us-central1-docker.pkg.dev/$(PROJECT_NAME)/$(ARTIFACT_REGISTORY_REPOSITORY_NAME)/$(IMAGE_NAME_WITH_TAG)


.PHONY: build
build:
	docker build . --tag $(IMAGE_URL)


.PHONY: push
push:
	docker push $(IMAGE_URL)


.PHONY: deploy_cloud_run
deploy_cloud_run:
	gcloud run services replace service.yaml
