import os
import sys
import subprocess

print("install.py running")
def failure(str):
    print("You need local admin or contact helpdesk. %s" % str)
    sys.exit(1)

def dependencies():
    if os.system("/usr/local/bin/brew --version") > 1:
        failure('brew version')

    print("Requiring sudo. Please enter your password to continue")

    if os.system("sudo echo \"Elevated Test Success!\"") > 1:
        failure('sudo check')

def ispath(path):
    with open(path) as f:
        if '/opt/local/bin' in f.read():
            return True
        return False

def makeprof(user, filename):
    print("Found %s for %s" % (filename, user))
    os.system("echo 'export PATH=\"/opt/local/bin:%s:$PATH\"' >> /Users/%s/%s" % (os.path.dirname(__file__), user, filename))
    os.system("echo 'eval $(minikube docker-env)' >> /Users/%s/%s" % (user, filename))

def setup_profile():
    print("Modifying PATH for All Users")
    for user in os.listdir('/Users/'):
        if user[0:1] != '.':
            if os.path.isfile("/Users/%s/.profile" % user) and ispath("/Users/%s/.profile" % user) == False:
                makeprof(user, '.profile')
            if os.path.isfile("/Users/%s/.bash_profile" % user) and ispath("/Users/%s/.bash_profile" % user) == False:
                makeprof(user, '.bash_profile')
            elif os.path.isfile("/Users/%s/.bashrc" % user) and ispath("/Users/%s/.bashrc" % user) == False:
                makeprof(user, '.bashrc')
            if os.path.isfile("/Users/%s/.zshrc" % user) and ispath("/Users/%s/.zshrc" % user) == False:
                makeprof(user, '.zshrc')
print("initialized functions")
try:
    docker_process = subprocess.check_output(['pgrep', 'Docker.app']).decode('UTF-8')[0:-1]
except subprocess.CalledProcessError:
    docker_process = None

dependencies()
if os.path.isdir("/Applications/Docker.app") and docker_process != None:
    os.system("sudo /Applications/Docker.app/Contents/MacOS/Docker --uninstall")

if os.system("sudo mkdir -p /opt/local/bin") > 1:
    failure('mkdir')

if os.system("install minikube-darwin-amd64 /opt/local/bin/minikube") > 1:
    failure('minikube install')
# if os.system("/usr/local/bin/brew install minikube docker docker-compose") > 1:
#     failure('brew install')


if os.system("cp %s/docker %s/docker-compose %s/docker-machine-driver-hyperkit /opt/local/bin/" % (os.path.dirname(__file__), os.path.dirname(__file__), os.path.dirname(__file__))) > 1:
    failure('docker docker-compose docker-machine-driver-hyperkit')

if os.system("sudo cp %s/hyperkit %s/vpnkit /opt/local/bin/" % (os.path.dirname(__file__), os.path.dirname(__file__))) > 1:
    failure('cp hyperkit')
if os.system("sudo chmod 755 /opt/local/bin/hyperkit /opt/local/bin/vpnkit") > 1:
    failure('chmod')
if os.system("sudo cp %s/*.plist /Library/LaunchDaemons/" % os.path.dirname(__file__)) > 1:
    failure('cp vpnkit.plist')
if os.system("sudo launchctl load -w /Library/LaunchDaemons/com.coredigital.vpnkit.plist") > 1:
    failure('launchctl vpnkit')

if setup_profile() != True:
    print("PATH failed to setup, using inline modification")
    os.system("export PATH=\"/opt/local/bin:$PATH\"")


# user = subprocess.check_output(['id', '-un']).decode('UTF-8')[0:-1]
# pwd = subprocess.check_output(['pwd']).decode('UTF-8')
# for user in os.listdir('/Users/'):
#         if user[0:1] != '.':
#             cwd = "/Users/%s" % user

#             cmd_env = {"PATH": "/opt/local/bin:/usr/local/bin:$PATH", "HOME": cwd, "USER": user}

#             subprocess.run(['start-minikube.sh'], env=cmd_env)

# if os.system("PATH=\"/opt/local/bin:$PATH\" start-minikube.sh") > 1:
#     failure('start-minikube')
# os.system("PATH=\"/opt/local/bin:$PATH\" minikube kubectl -- get pods -A")
# os.system("PATH=\"/opt/local/bin:$PATH\" minikube stop")

# if os.system("sudo launchctl load -w /Library/LaunchDaemons/com.coredigital.minikubedocker.plist") > 1:
#     failure('launchctl minikube docker')
# os.system("osascript -e 'tell application \"System Events\" to make login item at end with properties {name:\"Minikube Docker\", path:\"/Users/%s/bin/start-minikube.sh\", hidden:true}'")
