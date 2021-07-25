#!/usr/bin/env bash

export buildDir=/home/tungdt/go/src/github.com/daominah/minah_struture
export gitURL=git@github.com:daominah/minah_struture.git
export dockerImgTag=daominah/minah_struture

mkdir -p ${buildDir}
cd ${buildDir} && git clone ${gitURL} . 2>/dev/null;
cd ${buildDir} && git pull


cd ${buildDir} &&\
        docker build --tag=${dockerImgTag} --file=${buildDir}/Dockerfile .
if [[ $? -eq 0 ]]; then
    echo "built image ${dockerImgTag} with cache"
else
    cd ${buildDir} &&\
        docker build --tag=${dockerImgTag} --file=${buildDir}/Dockerfile --no-cache .
    echo "built image ${dockerImgTag} with no cache"
fi
