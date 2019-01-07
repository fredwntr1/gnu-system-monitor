import psutil
from PyQt4 import QtCore
from collections import Counter



def idk():
    cpu_percent = psutil.cpu_percent(percpu=True)
    core_count = len(cpu_percent)
    return cpu_percent




