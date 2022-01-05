import os
import sys

def failure():
    print("You need local admin or contact helpdesk.")
    sys.exit(1)

print("Requiring sudo. Please enter your password to continue")


os.system("minikube stop")
os.system("minikube delete")
if os.system("launchctl remove com.coredigital.vpnkit") > 1:
    failure()
os.system("sudo rm /opt/local/bin/hyperkit /opt/local/bin/vpnkit")
os.system("sudo rm /Library/LaunchDaemons/com.coredigital.vpnkit.plist")
remove_docker = input("Do you want to remove minikube, docker, and docker-compose? N/y ")
if remove_docker.lower() == "y":
    os.system("brew uninstall minikube docker docker-compose")