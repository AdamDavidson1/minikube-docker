import os
import sys

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
    print("Modifying PATH")
    if os.path.isfile("~/.profile"):
        os.system("echo 'export PATH=\"/opt/local/bin:$PATH\"' >> ~/.profile")
        os.system("source ~/.profile")
        return True
    elif os.path.isfile("~/.bash_profile"):
        os.system("echo 'export PATH=\"/opt/local/bin:$PATH\"' >> ~/.bash_profile")
        os.system("source ~/.bash_profile")
        return True
    elif os.path.isfile("~/.bashrc"):
        os.system("echo 'export PATH=\"/opt/local/bin:$PATH\"' >> ~/.bashrc")
        os.system("source ~/.bashrc")
        return True
    elif os.path.isfile("~/.zshrc"):
        os.system("echo 'export PATH=\"/opt/local/bin:$PATH\"' >> ~/.zshrc")
        os.system("source ~/.zshrc")
        return True
    return False

dependencies()
if os.path.isdir("/Applications/Docker.app"):
    os.system("sudo /Applications/Docker.app/Contents/MacOS/Docker --uninstall")

if os.system("brew install minikube docker docker-compose") > 1:
    failure()

if os.system("sudo mkdir -p /opt/local/bin") > 1:
    failure()
if os.system("sudo cp hyperkit vpnkit /opt/local/bin/") > 1:
    failure()
if os.system("sudo chmod 755 /opt/local/bin/hyperkit /opt/local/bin/vpnkit") > 1:
    failure()
if os.system("sudo cp vpnkit.plist /Library/LaunchDaemons/com.coredigital.vpnkit.plist") > 1:
    failure()
if os.system("sudo launchctl load -w /Library/LaunchDaemons/com.coredigital.vpnkit") > 1:
    failure()

if setup_profile() != True:
    print("PATH failed to setup, using inline modification")
    os.system("export PATH=\"/opt/local/bin:$PATH\"")

if os.system("minikube start --driver=hyperkit --hyperkit-vpnkit-sock=/var/run/vpnkit.socket") > 1:
    failure()
os.system("minikube kubectl -- get pods -A")
os.system("minikube stop")
if os.system("sudo cp minikube.plist /Library/LaunchDaemons/com.coredigital.minikubemachine.plist") > 1:
    failure()
if os.system("sudo launchctl load -w /Library/LaunchDaemons/com.coredigital.minikubemachine") > 1:
    failure()