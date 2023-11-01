#!/usr/bin/env bash
# Command for running tests locally in containers.

compose_version=$(docker-compose version|grep docker-compose|sed -n 's/.*version \([1-2]\).*/\1/p')
set -x

service_name=integration_service_test

declare -a COMPOSE_FILES=("-f docker-compose.tests.yml")
docker-compose ${COMPOSE_FILES} run --rm -v $PWD:/app/ "$service_name" "$@"

result=$?
docker-compose ${COMPOSE_FILES} down
exit $result

