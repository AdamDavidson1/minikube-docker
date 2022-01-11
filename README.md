# Minikube Docker installer
## Dependencies
- Homebrew
- python3
- python-tk

## Setup
First you need to install homebrew: [Homebrew](https://brew.sh/)

Next you will want to install python and Tcl/TK for python
```bash
$ brew install python@3.9 python-tk@3.9 
```

## Building
```bash
$ ./build.sh
```

## Installing
```bash
$ sudo installer -dumplog -pkg Minikube\ Docker.pkg -target /
```

## Debugging installation
```bash
$ cat /var/log/minikube_install.log
```

## Upgrading docker, docker-compose, hyperkit, vpnkit, minikube, docker-machine-driver-hyperkit 
### docker
You can download a new binary here: [docker](https://download.docker.com/mac/static/stable/)
### docker-compose
You can download a new binary here: [docker-compose](https://github.com/docker/compose/releases)
### hyperkit
You can download a new binary here: [hyperkit](https://github.com/moby/hyperkit)

Likely this will require to be compiled since moby has not built in a long time.
### vpnkit
You can download a new binary here: [vpnkit](https://github.com/moby/vpnkit)

Likely this will require to be compiled since moby has not built in a long time.
### minikube
You can download a new x86 binary here: [minikube](https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64)

for ARM: [minikube-arm](https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64)
### docker-machine-driver-hyperkit
You can download a new binary here: [docker-machine-driver-hyperkit](https://github.com/machine-drivers/docker-machine-driver-hyperkit/releases)