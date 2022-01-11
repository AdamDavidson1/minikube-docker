#!/bin/sh

rm -r dist
python3 setup.py py2app
cp start-minikube.sh dist/Minikube\ Docker.app/Contents/Resources/
rm Minikube\ Docker.pkg
pkgbuild --component "dist/Minikube Docker.app" --install-location "/Applications" --scripts ./scripts Minikube\ Docker.pkg
# productbuild --component "dist/Minikube Docker.app" "/Applications" --scripts ./scripts Minikube\ Docker.pkg
rm -r dist