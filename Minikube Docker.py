import os
import sys
import subprocess
import tkinter as tk
from tkinter import Text
from tkinter.constants import CENTER, INSERT, LEFT, RIGHT

user = subprocess.check_output(['id', '-un']).decode('UTF-8')[0:-1]
pwd = subprocess.check_output(['pwd']).decode('UTF-8')
cwd = f"/Users/{user}"
cmd_env = {"PATH": f"/opt/local/bin:/usr/local/bin:{pwd}:$PATH", "HOME": cwd, "USER": user, "CHANGE_MINIKUBE_NONE_USER": "false"}
if os.system("osascript -e 'tell application \"System Events\" to get the name of every login item' | grep start-minikube.sh") < 0:
    os.system("osascript -e 'tell application \"System Events\" to make login item at end with properties {name:\"Minikube Docker\", path:\"%s/start-minikube.sh\", hidden:true}'" % pwd)



root = tk.Tk()
text = Text(root, width=150)
start_status = Text(root, width=150)
status = "Unknown"
def poll_for_data():
    output = subprocess.run(['minikube', 'status'], env=cmd_env, cwd=cwd, capture_output=True)
    if output.stderr.decode('UTF-8') != "":
        status = f"Not Running \n{output.stdout.decode('UTF-8')} \n {output.stderr.decode('UTF-8')}"
    else:
        status = f"Running \n {output.stdout.decode('UTF-8')}"

    ip = subprocess.run(['minikube', 'ip'], env=cmd_env, cwd=cwd, capture_output=True)
    if ip.stderr.decode('UTF-8') != "":
        status = f"{status} \n Error getting ip: {ip.stdout.decode('UTF-8')} \n {ip.stderr.decode('UTF-8')}"
    else:
        status = f"{status} \n DNS local.cdm routes to {ip.stdout.decode('UTF-8')}"

    text.delete("1.0", "end")
    text.insert(INSERT, f"System Status: {status}")
    root.after(3000, poll_for_data)

def start():
    start_status.delete("1.0", "end")
    try:
        # output = subprocess.run(['minikube', 'start', '--mount-ip=192.168.64.20', '--driver=hyperkit', '--hyperkit-vpnkit-sock=/var/run/vpnkit.socket'], env=cmd_env, cwd=cwd, capture_output=True)
        output = subprocess.run(['start-minikube.sh'], env=cmd_env, cwd=cwd, capture_output=True)
        start_status.insert(INSERT, f"{output.stdout.decode('UTF-8')} \n {output.stderr.decode('UTF-8')}")
        if output.stdout.find("minikube kubectl -- get pods -A") >= 0:
            output = subprocess.run(['minikube', 'kubectl', '--', 'get', 'pods', '-A'], env=cmd_env, cwd=cwd, capture_output=True)
            start_status.insert(INSERT, f"{output.stdout.decode('UTF-8')} \n {output.stderr.decode('UTF-8')}")

    except subprocess.CalledProcessError as err:
        start_status.insert(INSERT, f"{err.stdout.decode('UTF-8')}")

def delete():
    start_status.delete("1.0", "end")
    try:
        output = subprocess.run(['minikube', 'delete'], env=cmd_env, cwd=cwd, capture_output=True)
        start_status.insert(INSERT, f"{output.stdout.decode('UTF-8')} \n {output.stderr.decode('UTF-8')}")
    except subprocess.CalledProcessError as err:
        start_status.insert(INSERT, f"{err.stdout.decode('UTF-8')}")

def stop():
    start_status.delete("1.0", "end")
    try:
        output = subprocess.run(['minikube', 'stop'], env=cmd_env, cwd=cwd, capture_output=True)
        start_status.insert(INSERT, f"{output.stdout.decode('UTF-8')} \n {output.stderr.decode('UTF-8')}")
    except subprocess.CalledProcessError as err:
        start_status.insert(INSERT, f"{err.stdout.decode('UTF-8')}")

# put the poller on the main loop the first time
root.after(1000, poll_for_data)
root.title("Minikube Docker")
text.insert(INSERT, f"System Status: {status}")
text.pack(padx=10, pady=10)
start_status.pack(padx=10, pady=10)
tk.Button(root, text="Start Minikube Cluster", command=start).pack(side=LEFT)
tk.Button(root, text="Stop Minikube Cluster", command=stop).pack(side=LEFT)
tk.Button(root, text="Delete Minikube Cluster", command=delete).pack(side=RIGHT)
tk.mainloop()