import sys
import mem_stats
from PyQt4 import QtCore, QtGui
import ui
import mem_worker
import cpu_worker
import gpu_worker





class MemProcessTableWorker(QtCore.QThread):
    def __init__(self):
        super(MemProcessTableWorker, self).__init__()
     #   self.signal = MemWorkerSignal()

    def run(self):
        pid_table = mem_stats.mem_procs()
        pid_count = mem_stats.num_of_procs()
        self.emit(QtCore.SIGNAL('PROC_STATS'),pid_table, pid_count)






if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    app = MainClass()
    app.show()
    sys.exit(a.exec_())