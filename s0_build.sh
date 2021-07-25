#!/usr/bin/env bash

set -e

export machines=(smsgtel0)

export deployDir=/home/tungdt/go/src/github.com/daominah/minah_struture

for machine in ${machines[@]}; do
    echo "building docker image on ${machine}"
    docker-machine ssh ${machine} "mkdir -p ${deployDir}; cd ${deployDir}; /usr/bin/git pull"
    docker-machine ssh ${machine} /bin/bash ${deployDir}/s1_build_local.sh &
done
wait
echo "built docker image on all machines"
