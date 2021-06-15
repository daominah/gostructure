#!/usr/bin/env bash

set -e

export machines=(masdev0 masdev1 masdev2)

export buildDir=/home/tungdt/go/src/github.com/daominah/minah_struture

for machine in ${machines[@]}; do
    echo "building docker image on ${machine}"
    docker-machine ssh ${machine} /bin/bash ${buildDir}/s1_build_local.sh &
done
wait
echo "built docker image on all machines"
