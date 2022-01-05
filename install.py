import os
import sys
import subprocess
import re

def failure():
    print("You need local admin or contact helpdesk.")
    sys.exit(1)

def dependencies():
    if os.system("brew --version") > 1:
        failure()

    print("Requiring sudo. Please enter your password to continue")

    if os.system("sudo echo \"Elevated Test Success!\"") > 1:
        failure()

def setup_profile():
    if os.environ.get("PATH").find("/opt/local/bin") > -1:
        return True
    print("Modifying PATH")
    user = subprocess.check_output(['id', '-un']).decode('UTF-8')[0:-1]
    if os.path.isfile(f"/User/{user}/.profile"):
        os.system(f"echo 'export PATH=\"/opt/local/bin:$PATH\"' >> /User/{user}/.profile")
        os.system(f"source /User/{user}/.profile")
        return True
    elif os.path.isfile(f"/User/{user}/.bash_profile"):
        os.system(f"echo 'export PATH=\"/opt/local/bin:$PATH\"' >> /User/{user}/.bash_profile")
        os.system(f"source /User/{user}/.bash_profile")
        return True
    elif os.path.isfile(f"/User/{user}/.bashrc"):
        os.system(f"echo 'export PATH=\"/opt/local/bin:$PATH\"' >> /User/{user}/.bashrc")
        os.system(f"source /User/{user}/.bashrc")
        return True
    elif os.path.isfile(f"/User/{user}/.zshrc"):
        os.system(f"echo 'export PATH=\"/opt/local/bin:$PATH\"' >> /User/{user}/.zshrc")
        os.system(f"source /User/{user}/.zshrc")
        return True
    return False

user = subprocess.check_output(['id', '-un']).decode('UTF-8')[0:-1]

dependencies()
if os.path.isdir("/Applications/Docker.app") and input("Do you have Docker Desktop Installed? N/y ").lower() == 'y':
    os.system("sudo /Applications/Docker.app/Contents/MacOS/Docker --uninstall")

if os.system("brew install minikube docker docker-compose") > 1:
    failure()
os.system(f"mkdir -p /Users/{user}/bin")
os.system(f"cp start-minikube.sh /Users/{user}/bin/")

if os.system("sudo mkdir -p /opt/local/bin") > 1:
    failure()
if os.system("sudo cp hyperkit vpnkit /opt/local/bin/") > 1:
    failure()
if os.system("sudo chmod 755 /opt/local/bin/hyperkit /opt/local/bin/vpnkit") > 1:
    failure()
if os.system("sudo cp com.coredigital.vpnkit.plist /Library/LaunchDaemons/") > 1:
    failure()
if os.system("launchctl load -w /Library/LaunchDaemons/com.coredigital.vpnkit.plist") > 1:
    failure()

if setup_profile() != True:
    print("PATH failed to setup, using inline modification")
    os.system("export PATH=\"/opt/local/bin:$PATH\"")

if os.system("minikube status") == 0:
    print("Existing cluster was found!")
    print("Please run: minikube stop && minikube delete and try again.")
    sys.exit(2)
if os.system("~/bin/start-minikube.sh") > 1:
    failure()
os.system("minikube kubectl -- get pods -A")
os.system("osascript -e 'tell application \"System Events\" to make login item at end with properties {name:\"Minikube Docker\", path:\"/User/" + user + "/bin/start-minikube.sh\", hidden:true}'")