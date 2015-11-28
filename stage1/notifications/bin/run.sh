#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:$portToUse --name notifications$portToUse \
    -e portToUse=$portToUse \
    -v $PWD/datavol:/notifications/datavol \
    -d dsanders/notifications /bin/bash -c /notifications/startup.sh \
