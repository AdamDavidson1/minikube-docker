#!/bin/sh

export PATH="/opt/local/bin:$PATH"
export MINIKUBE_UUID=
echo $PATH
minikube start --uuid=$MINIKUBE_UUID --driver=hyperkit --hyperkit-vpnkit-sock=/var/run/vpnkit.socket