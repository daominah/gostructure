#!/usr/bin/env bash

export machines=(masdev0 masdev1 masdev2)

export dockerImgTag=minah_struture
export dockerCtnName=minah_struture


# clean up old container
for machine in ${machines[@]}; do
    eval $(docker-machine env ${machine})
    echo "stop and remove old container ${dockerCtnName} in ${machine}"
    docker stop -t 2 ${dockerCtnName} 2>/dev/null;
    docker rm ${dockerCtnName} 2>/dev/null;
    eval $(docker-machine env --unset)
done


set -e
# sequentially docker run on machines
for i in ${!machines[@]}; do
    eval $(docker-machine env ${machines[i]})

    echo "preparing env vars for ${dockerCtnName} on node $(docker-machine active)"
    export cfgFile=./conf/env.sh
    dkrEnv=${PWD}/env_docker_run.list${i}; bash -x ${cfgFile} 2>${dkrEnv}
    sed -i 's/+ //' ${dkrEnv}; sed -i '/^export /d' ${dkrEnv}; sed -i "s/'//g" ${dkrEnv}

    docker run -dit --name ${dockerCtnName} \
        --env-file ${dkrEnv} \
        --network host \
        ${dockerImgTag}
    sleep 1

    eval $(docker-machine env --unset)
done
