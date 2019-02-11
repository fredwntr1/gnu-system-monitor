import time
from PyQt5 import QtCore
import cpu_stats
import multiprocessing


class CpuWorkerSignals(QtCore.QObject):
    cpu_worker_signal = QtCore.pyqtSignal(int, str, int)
    cpu_table_signal = QtCore.pyqtSignal(list, int, list)
    cpu_graph_signal = QtCore.pyqtSignal(int, list)
    p2 = multiprocessing.Pool(processes=1)


class CpuWorker(QtCore.QThread):
    def __init__(self):
        super(CpuWorker, self).__init__()
        self.stats_signal = CpuWorkerSignals()

    def run(self):
        while True:
            temp = self.stats_signal.p2.apply(cpu_stats.cpu_temp)
            cpu_percent = self.stats_signal.p2.apply(cpu_stats.cpu_load_percentage)
            fan = self.stats_signal.p2.apply(cpu_stats.cpu_fan)
            self.stats_signal.cpu_worker_signal.emit(cpu_percent, temp, fan)
            QtCore.QCoreApplication.processEvents()
            time.sleep(2)


class CpuTable(QtCore.QThread):
    def __init__(self):
        super(CpuTable, self).__init__()
        self.table_signal = CpuWorkerSignals()

    def run(self):
        while True:
            core_count = self.table_signal.p2.apply(cpu_stats.list_cpus)
            cpu_freq = self.table_signal.p2.apply(cpu_stats.cpu_clock_speed)
            cpu_percent = self.table_signal.p2.apply(cpu_stats.total_cpu_percentage)
            self.table_signal.cpu_table_signal.emit(cpu_freq, core_count, cpu_percent)
            QtCore.QCoreApplication.processEvents()
            time.sleep(2)


class CpuGraphWorker(QtCore.QThread):
    def __init__(self):
        super(CpuGraphWorker, self).__init__()
        self.graph_signal = CpuWorkerSignals()

    def run(self):
        while True:
            core_count = self.graph_signal.p2.apply(cpu_stats.list_cpus)
            cpu_load = self.graph_signal.p2.apply(cpu_stats.total_cpu_percentage)
            self.graph_signal.cpu_graph_signal.emit(core_count, cpu_load)
            QtCore.QCoreApplication.processEvents()
            time.sleep(1)
