import os
import sys
import subprocess

source = sys.argv[1]
print("Moving from %s" % source)

def ispath(path):
    with open(path) as f:
        if '/opt/local/bin' in f.read():
            return True
        return False

def move_state(user):
    print("Moving to user %s" % user)
    os.system("cp -r %s/.minikube /Users/%s/" % (source.replace(" ", "\ "), user))
    os.system("cp -r %s/.kube /Users/%s/" % (source.replace(" ", "\ "), user))
    os.system("chown -R %s /Users/%s/.minikube /Users/%s/.kube" % (user, user, user))
    os.system("chown root:wheel /Users/%s/.minikube/bin/docker-machine-driver-hyperkit" % user)
    os.system("chmod u+s /Users/%s/.minikube/bin/docker-machine-driver-hyperkit" % user)

for user in os.listdir('/Users/'):
    if user[0:1] != '.' and user.lower() != "cdmadmin":
        user_dir = os.listdir("/Users/%s" % user)
        try:
            if user_dir.index("Desktop"):
                move_state(user)
        except ValueError:
            print("Skipping %s" % user)