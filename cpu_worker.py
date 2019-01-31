import time
from PyQt4 import QtCore
import cpu_stats


class CpuWorkerSignals(QtCore.QObject):
    cpu_worker_signal = QtCore.pyqtSignal(int, str, int)
    cpu_table_signal = QtCore.pyqtSignal(list, int, list)
    cpu_graph_signal = QtCore.pyqtSignal(int, list)


class CpuWorker(QtCore.QRunnable):
    def __init__(self):
        super(CpuWorker, self).__init__()
        self.stats_signal = CpuWorkerSignals()

    def run(self):
        while True:
            temp = cpu_stats.cpu_temp()
            cpu_percent = cpu_stats.cpu_load_percentage()
            fan = cpu_stats.cpu_fan()
            self.stats_signal.cpu_worker_signal.emit(cpu_percent, temp, fan)
            time.sleep(2)
            QtCore.QCoreApplication.processEvents()


class CpuTable(QtCore.QRunnable):
    def __init__(self):
        super(CpuTable, self).__init__()
        self.table_signal = CpuWorkerSignals()

    def run(self):
        while True:
            core_count = cpu_stats.list_cpus()
            cpu_freq = cpu_stats.cpu_clock_speed()
            cpu_percent = cpu_stats.total_cpu_percentage()
            self.table_signal.cpu_table_signal.emit(cpu_freq, core_count, cpu_percent)
            time.sleep(2)
            QtCore.QCoreApplication.processEvents()


class CpuGraphWorker(QtCore.QRunnable):
    def __init__(self):
        super(CpuGraphWorker, self).__init__()
        self.graph_signal = CpuWorkerSignals()

    def run(self):
        while True:
            core_count = cpu_stats.list_cpus()
            cpu_load = cpu_stats.total_cpu_percentage()
            self.graph_signal.cpu_graph_signal.emit(core_count, cpu_load)
            time.sleep(2)
            QtCore.QCoreApplication.processEvents()

