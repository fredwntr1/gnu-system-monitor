from PyQt4 import QtCore, QtGui
import ui
import time
import cpu_stats
import multiprocessing
import pyqtgraph
import numpy as np
import psutil


class MainClass(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent= None):
        super(MainClass, self).__init__(parent)
        self.setupUi(self)
        self.threadclass = ThreadClass()
        self.threadclass.start()
        self.cpu_percentage_graph.setDownsampling(mode='peak')
        self.cpu_percentage_graph.setClipToView(True)
        self.connect(self.threadclass, QtCore.SIGNAL('CPU_STATS'), self.update_cpu_graph)
        self.cpu_percentage_graph.setLabel('left', 'value', units='%')
        self.cpu_percentage_graph.setYRange(0, 100)
        self.cpu_percentage_graph.setXRange(0, cpu_stats.list_cpus())

    def update_cpu_graph(self, cpu_load):
        y1 = np.linspace(0, 20, cpu_stats.list_cpus())
        cpu_bar_item = pyqtgraph.BarGraphItem(x=cpu_load, height=y1, width=0.6, brush='r')
        self.cpu_percentage_graph.addItem(cpu_bar_item)







class ThreadClass(QtCore.QThread):
    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        import graph_worker
        while True:
            cpu_load = graph_worker.idk()
            self.emit(QtCore.SIGNAL('CPU_STATS'), cpu_load)
            time.sleep(2)


if __name__ == '__main__':
    import sys
    a = QtGui.QApplication(sys.argv)

    app = MainClass()
    app.show()
    sys.exit(a.exec_())