CURRENT_USER_ID:=$(shell id -u)
export CURRENT_USER_ID

CURRENT_GROUP_ID:=$(shell id -g)
export CURRENT_GROUP_ID

INTERACTIVE:=$(shell [ -t 0 ] && echo 1)
ifdef INTERACTIVE
	DOCKER_RUN_TTY_ARG := -it
endif

define COMPOSE_FILES
    -f docker-compose.yml
endef

ACCEPTARGSGOALS := devcodestylecheck devcodestyleformat
HOST_LOG_DIRECTORY := "/tmp/integration-logs"
CONTAINER_LOG_DIRECTORY := "/var/log"


# If the first argument in ACCEPTARGSGOALS
ifneq ($(filter $(firstword $(MAKECMDGOALS)),$(ACCEPTARGSGOALS)),)
  # use the rest as arguments
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # turn them into blank targets
  $(eval $(RUN_ARGS):;@:)
endif


CODESTYLEIMIGENAME ?= codestyle

.PHONY: devcodestylecheck
devcodestylecheck:
	cd codestyle && \
	docker build -t $(CODESTYLEIMIGENAME) . && \
	docker run $(DOCKER_RUN_TTY_ARG) --rm --volume "${PWD}:/code" $(CODESTYLEIMIGENAME) check $(RUN_ARGS)

.PHONY: devcodestyleformat
devcodestyleformat:
	cd codestyle && \
	docker build -t $(CODESTYLEIMIGENAME) . && \
	docker run $(DOCKER_RUN_TTY_ARG) --rm --volume "${PWD}:/code" --user "${CURRENT_USER_ID}:${CURRENT_GROUP_ID}" $(CODESTYLEIMIGENAME) format $(RUN_ARGS)


.PHONY: devtest
devtest:
	./run_tests_in_docker.sh


.PHONY: devup
devup:
	mkdir -p ${HOST_LOG_DIRECTORY} && \
	CONTAINER_LOG_DIRECTORY=${CONTAINER_LOG_DIRECTORY} HOST_LOG_DIRECTORY=${HOST_LOG_DIRECTORY} docker-compose ${COMPOSE_FILES} up --build -d


.PHONY: devdown
devdown:
	CONTAINER_LOG_DIRECTORY=${CONTAINER_LOG_DIRECTORY} HOST_LOG_DIRECTORY=${HOST_LOG_DIRECTORY} docker-compose ${COMPOSE_FILE} down --remove-orphans $(RUN_ARGS)