PROJECT = chalkhorn
ID = pikesley/${PROJECT}

all: build

build:
	docker build \
		--tag ${ID} .

run:
	docker run \
		--interactive \
		--tty \
		--name ${PROJECT} \
		--volume $(shell pwd)/${PROJECT}:/opt/${PROJECT} \
		--volume ${HOME}/.ssh:/root/.ssh \
		--rm \
		${ID} bash
