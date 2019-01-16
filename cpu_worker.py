import time
from PyQt4 import QtCore
import cpu_stats


class CpuWorker(QtCore.QThread):
    def __init__(self):
        super(CpuWorker, self).__init__()

    def run(self):
        while True:
            temp = cpu_stats.cpu_temp()
            cpu_percent = cpu_stats.cpu_load_percentage()
            fan = cpu_stats.cpu_fan()
            self.emit(QtCore.SIGNAL("CPU_STATS"), cpu_percent, temp, fan)
            time.sleep(1)


class CpuTable(QtCore.QThread):
    def __init__(self):
        super(CpuTable, self).__init__()

    def run(self):
        while True:
            #core_count = cpu_stats.list_cpus()
            cpu_freq = cpu_stats.cpu_clock_speed()
            self.emit(QtCore.SIGNAL("CPU_TABLE"), cpu_freq)
            time.sleep(1)
