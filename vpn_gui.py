from tkinter import *
from tkinter import ttk
import subprocess
import time
import os

pid = None
dir = os.path.dirname(os.path.abspath('__main__'))
sudo_password = "Password@tech"
vpn_filename = "Sushant_Yadav.ovpn"
openvpn_file_path = dir+"/"+vpn_filename
vpn_pass_file_path = dir+"/pass_vpn"   # file having password of your vpn

def action():
    global pid, button
    if not pid:
        proc = subprocess.Popen(f'echo "{sudo_password}" | sudo -S -k openvpn --client --config {openvpn_file_path} --askpass {vpn_pass_file_path}',
                                    shell=True,
                                    stdin=subprocess.PIPE, 
                                    # stdout=subprocess.PIPE, 
                                    # stderr=subprocess.PIPE
                                    )
        pid = proc.pid
        button['text'] = "Turn Off"
        print("Vpn activated :", pid)
    else:
        pids = subprocess.check_output("pidof openvpn".split()).decode().split()
        print("Pids :", pids)
        for pid in pids:
            proc = subprocess.Popen(f'echo "{sudo_password}" | sudo -S -k kill -9 {pid}', shell=True)
            print(proc.wait())
            print(f'pid {pid} killed')
        time.sleep(1)
        try:
            pids = subprocess.check_output("pidof openvpn".split())
            print("Pids (after turn off attempt) :", pids)
        except subprocess.CalledProcessError:
            pids = None
        if not pids:
            pid = None
            button['text'] = "Turn On"
            print("Vpn de-activated.")
        else:
            print("Failed to turn off.")

root = Tk()
root.title("Itilite VPN")
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Control VPN").grid(column=0, row=0)
ttk.Label(frm, text="").grid(column=0, row=1)
button = Button(frm, text="Turn On", command=action)
# button.pack()
button.grid(column=0, row=2)
root.mainloop()