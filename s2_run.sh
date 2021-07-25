#!/usr/bin/env bash

export machines=(smsgtel0)

export dockerImgTag=daominah/minah_struture
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

    echo "preparing envs specific to node for ${dockerCtnName} on $(docker-machine active)"
    dkrEnv=${PWD}/env_docker_run.list${i}; bash -x ./env.sh 2>${dkrEnv}
    sed -i 's/+ //' ${dkrEnv}; sed -i '/^export /d' ${dkrEnv}; sed -i "s/'//g" ${dkrEnv}

    docker run -dit --restart always --name ${dockerCtnName} \
        --env-file ${dkrEnv} \
        --network host \
        ${dockerImgTag}
    sleep 2

    eval $(docker-machine env --unset)
    echo "ok run ${dockerCtnName} on ${machines[i]}"
done
