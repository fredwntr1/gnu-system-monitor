import time
from PyQt4 import QtCore
import cpu_stats



#class CpuWorkerSignal(QtCore.QObject):
 #   worker_signal = QtCore.pyqtSignal(int, float, float)



class CpuWorker(QtCore.QThread):
    def __init__(self):
        super(CpuWorker, self).__init__()
     #   self.signal = CpuWorkerSignal()

    def run(self):
        while True:
            if cpu_stats.find_cpu() == repr('AMD'):
                cpu_temp = float(cpu_stats.amd_temp())
            elif cpu_stats.find_cpu() == repr('INT'):
                cpu_temp = float(cpu_stats.intel_temp())
            cpu_fan = cpu_stats.cpu_fan_rpm()
            cpu_percent = cpu_stats.cpu_load_percentage()
            self.emit(QtCore.SIGNAL("CPU_STATS"), cpu_fan, cpu_percent, cpu_temp)
            time.sleep(1)