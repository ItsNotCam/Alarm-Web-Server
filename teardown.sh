#!/bin/bash

# shutdown containers
docker-compose -f ${PWD}/docker/docker-compose.yml down

# remove networks
docker network rm dockernet -f

# remove image
docker image rm axiiom/acs:2.0 -f
