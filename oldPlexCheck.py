import os
import threading
import subprocess
from datetime import datetime


# make sure to chmod +x the script so that it can run the docker stop command
# i cbs outputting a log or putting into syslog so run script with screen to check print outputs

hostname = "x.x.x.x"  # put your hostname here
interval = 5  # set interval in seconds to send a ping
pingTimeout = 3  # in seconds how long to abort ping
pingCommand = "ping -c 1 -w {} {}".format(pingTimeout, hostname)


def startTimer():
    threading.Timer(interval, startTimer).start()
    mrPinger()


def mrPinger():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ["ping", "-c", "1", "-w", str(pingTimeout), hostname],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            print("responded to ping and is up")
            os.system("sudo docker stop plex")
            print("plex killed at: " + current_time)
            os._exit(1)
        except subprocess.CalledProcessError:
            print("server is still down at: " + current_time)


startTimer()
