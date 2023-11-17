# import daemon
from receiver import car_controlling_agent
from receiver import signal_start
import daemon

def do_something():
    while True:
        if signal_start:
            car_controlling_agent.refresh_car_action()
        else:
            car_controlling_agent.stop_car()

def init_daemon():
    with daemon.DaemonContext():
        do_something()
