#!/usr/bin/env bash

export dockerImgTag=minah_struture
export dockerCtnName=minah_struture


export buildDir=.
cd ${buildDir} &&\
        docker build --tag=${dockerImgTag} --file=${buildDir}/Dockerfile .
if [[ $? -eq 0 ]]; then
    echo "built image ${dockerImgTag} with cache"
else
    cd ${buildDir} &&\
        docker build --tag=${dockerImgTag} --file=${buildDir}/Dockerfile --no-cache .
    echo "built image ${dockerImgTag} with no cache"
fi


# clean up old container
echo "stop and remove old container ${dockerCtnName}"
docker stop ${dockerCtnName} 2>/dev/null;
docker rm ${dockerCtnName} 2>/dev/null;


echo "preparing envs"
export dkrEnv=${PWD}/env_docker_run.list; bash -x ./conf/env.sh 2>${dkrEnv}
sed -i 's/+ //' ${dkrEnv}; sed -i '/^export /d' ${dkrEnv}; sed -i "s/'//g" ${dkrEnv}

docker run -dit --name=${dockerCtnName} --restart always \
    --network=host \
    --env-file ${dkrEnv} \
    ${dockerImgTag}

echo "done run ${dockerCtnName} container"
