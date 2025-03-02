# Usage: make build push
DOCKER_USERNAME ?= tyzen9
APPLICATION_NAME ?= myanonamouse-ip-helper
 
build:
	docker buildx build --platform linux/amd64,linux/arm64 --tag ${DOCKER_USERNAME}/${APPLICATION_NAME} .

push:
	docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}