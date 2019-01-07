import time
from PyQt4 import QtCore

import mem_stats



class MemWorker(QtCore.QThread):
    def __init__(self):
        super(MemWorker, self).__init__()

    def run(self):
        while True:
            free_mem = mem_stats.free_mem()
            total_mem = mem_stats.total_mem()
            total_swap_mem = mem_stats.total_swap_mem()
            used_swap_mem = mem_stats.used_swap_mem()
            self.emit(QtCore.SIGNAL("MEM_STATS"), free_mem, total_mem, total_swap_mem, used_swap_mem)
            time.sleep(1)


class MemProcessTableWorker(QtCore.QThread):
    def __init__(self):
        super(MemProcessTableWorker, self).__init__()

    def run(self):
        while True:
            pid_table = mem_stats.mem_procs()
            proc_username = mem_stats.user_proc()
            process_percent = mem_stats.proc_cpu_percent()
            mem_percent = mem_stats.proc_mem_percent()
            mem_pid = mem_stats.proc_pids()
            self.emit(QtCore.SIGNAL('UPDATE_MEM_PROCS'), pid_table, proc_username, process_percent, mem_percent, mem_pid)
            time.sleep(1)







