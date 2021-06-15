#!/usr/bin/env bash

# this script will be called by s0_build.sh

export buildDir=/home/tungdt/go/src/github.com/daominah/minah_struture
export gitURL=git@github.com:daominah/minah_struture.git
export dockerImgTag=minah_struture

mkdir -p ${buildDir}
cd ${buildDir} && git clone ${gitURL} .
cd ${buildDir} && git pull

cd ${buildDir} &&\
        docker build --tag=${dockerImgTag} --file=${buildDir}/conf/Dockerfile .
if [[ $? -eq 0 ]]; then
    echo "built image ${dockerImgTag} with cache"
else
    cd ${buildDir} &&\
        docker build --tag=${dockerImgTag} --file=${buildDir}/conf/Dockerfile --no-cache .
    echo "built image ${dockerImgTag} with no cache"
fi
