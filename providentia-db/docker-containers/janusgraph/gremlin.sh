#!/bin/sh

docker run --rm --link prv-janusgraph:janusgraph -e GREMLIN_REMOTE_HOSTS=janusgraph -it --net janusgraph-docker_prv-network janusgraph/janusgraph:latest ./bin/gremlin.sh
