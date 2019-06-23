import psutil
import sys

def getPidList():
    list = []
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
            list.append("[{}]{}".format(pid, p.name()))
        except:
            pass
    return list