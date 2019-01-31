import time
from PyQt4 import QtCore
import mem_stats
import multiprocessing


class MemWorkerSignals(QtCore.QObject):
    mem_stats_signal = QtCore.pyqtSignal(int, int, int)
    mem_table_signal = QtCore.pyqtSignal(list, list, list, list, list)
    mem_graph_signal = QtCore.pyqtSignal(int, int, int)
    p1 = multiprocessing.Pool(processes=1)


class MemStats(QtCore.QThread):
    def __init__(self):
        super(MemStats, self).__init__()
        self.mem_worker_signal = MemWorkerSignals()

    def run(self):
        while True:
            free_mem = self.mem_worker_signal.p1.apply(mem_stats.free_mem)
            total_mem = self.mem_worker_signal.p1.apply(mem_stats.total_mem)
            total_swap_mem = self.mem_worker_signal.p1.apply(mem_stats.total_swap_mem)
            self.mem_worker_signal.mem_stats_signal.emit(free_mem, total_mem, total_swap_mem)
            QtCore.QCoreApplication.processEvents()
            time.sleep(2)


class MemProcessTableWorker(QtCore.QThread):
    def __init__(self):
        super(MemProcessTableWorker, self).__init__()
        self.mem_worker_signal = MemWorkerSignals()

    def run(self):
        while True:
            pid_table = self.mem_worker_signal.p1.apply(mem_stats.mem_procs)
            proc_username = self.mem_worker_signal.p1.apply(mem_stats.user_proc)
            process_percent = self.mem_worker_signal.p1.apply(mem_stats.proc_cpu_percent)
            mem_percent = self.mem_worker_signal.p1.apply(mem_stats.proc_mem_percent)
            mem_pid = self.mem_worker_signal.p1.apply(mem_stats.proc_pids)
            self.mem_worker_signal.mem_table_signal.emit(pid_table, proc_username, process_percent, mem_percent, mem_pid)
            QtCore.QCoreApplication.processEvents()
            time.sleep(2)


class MemGraphWorker(QtCore.QThread):
    def __init__(self):
        super(MemGraphWorker, self).__init__()
        self.mem_worker_signal = MemWorkerSignals()

    def run(self):
        while True:
            used_mem = self.mem_worker_signal.p1.apply(mem_stats.used_mem)
            free_mem = self.mem_worker_signal.p1.apply(mem_stats.free_mem_percent)
            used_swap = self.mem_worker_signal.p1.apply(mem_stats.swap_percent)
            self.mem_worker_signal.mem_graph_signal.emit(used_mem, free_mem, used_swap)
            QtCore.QCoreApplication.processEvents()
            time.sleep(1)



