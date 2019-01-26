from PyQt4 import QtCore
import net_stats
import time


class NetProcessWorker(QtCore.QThread):
    def __init__(self):
        super(NetProcessWorker, self).__init__()

    def run(self):
        while True:
            net_processes = net_stats.net_procs()
            net_download = net_stats.net_proc_download()
            net_upload = net_stats.net_proc_upload()
            self.emit(QtCore.SIGNAL("NET_STATS"), net_processes, net_download, net_upload)
            time.sleep(3)
            QtCore.QCoreApplication.processEvents()

