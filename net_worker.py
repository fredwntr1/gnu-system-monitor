from PyQt5 import QtCore
import net_stats
import time


class NetThread(QtCore.QObject):
    net_proc_thread = QtCore.pyqtSignal(list, list, list)


class NetProcessWorker(QtCore.QThread):
    def __init__(self):
        super(NetProcessWorker, self).__init__()
        self.net_signal = NetThread()

    def run(self):
        while True:
            net_processes = net_stats.net_procs()
            net_download = net_stats.net_proc_download()
            net_upload = net_stats.net_proc_upload()
            self.net_signal.net_proc_thread.emit(net_processes, net_download, net_upload)
            QtCore.QCoreApplication.processEvents()
            time.sleep(3)
