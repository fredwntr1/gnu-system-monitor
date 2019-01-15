#!/usr/bin/env python3
import sys
from PyQt4 import QtCore, QtGui
import ui
import mem_worker
import cpu_worker
import gpu_worker
import net_worker
import pyqtgraph
import subprocess


class MainClass(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainClass, self).__init__()
        self.setupUi(self)
        self.mem_worker = mem_worker.MemWorker()
        self.mem_table = mem_worker.MemProcessTableWorker()
        self.cpu_worker = cpu_worker.CpuWorker()
        self.gpu_worker = gpu_worker.GpuWorker()
        self.net_worker = net_worker.NetProcessWorker()
        self.mem_worker.start()
        self.cpu_worker.start()
        self.gpu_worker.start()
        self.mem_table.start()
        self.net_worker.start()
        self.connect(self.mem_worker, QtCore.SIGNAL("MEM_STATS"), self.show_mem_stats)
        self.connect(self.cpu_worker, QtCore.SIGNAL("CPU_STATS"), self.show_cpu_stats)
        self.connect(self.gpu_worker, QtCore.SIGNAL("GPU_STATS"), self.show_gpu_stats)
        self.connect(self.mem_table, QtCore.SIGNAL('UPDATE_MEM_PROCS'), self.update_process_table)
        self.connect(self.net_worker, QtCore.SIGNAL("NET_STATS"), self.show_net_stats)
        self.process_table_widget.cellClicked.connect(self.choose_kill_process)
        self.end_task_pushbutton.clicked.connect(self.kill_process)
        self.net_limit_pushbutton.setEnabled(False)

    def show_net_stats(self, net_processes, net_download, net_upload):
        self.net_process_widget.setRowCount(len(net_processes))
        for i, row in enumerate(net_processes):
            self.net_process_widget.setItem(i, 0, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(net_download):
            self.net_process_widget.setItem(i, 1, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(net_upload):
            self.net_process_widget.setItem(i, 2, QtGui.QTableWidgetItem(row))

    def update_process_table(self, pid_table, proc_username, process_percent, mem_percent, mem_pid):
        self.process_table_widget.setRowCount(len(pid_table))
        for i, row in enumerate(pid_table):
            self.process_table_widget.setItem(i, 0, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(proc_username):
            self.process_table_widget.setItem(i, 1, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(process_percent):
            self.process_table_widget.setItem(i, 2, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(mem_percent):
            self.process_table_widget.setItem(i, 3, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(mem_pid):
            self.process_table_widget.setItem(i, 4, QtGui.QTableWidgetItem(row))

    def show_mem_stats(self, free_mem, total_mem, used_swap_mem):
        self.free_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.free_mem_label.setText("   %d" % free_mem)
        self.total_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.total_mem_label.setText("   %d" % total_mem)
        self.swap_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.swap_mem_label.setText("   %d" % used_swap_mem)

    def show_cpu_stats(self, cpu_fan, cpu_percent, cpu_temp):
        self.cpu_fan_speed_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.cpu_fan_speed_label.setText("%d RPM" % cpu_fan)
        self.cpu_temp_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.cpu_load_progressbar.setValue(cpu_percent)
        self.cpu_temp_label.setText("   %d C" % cpu_temp)

    def show_gpu_stats(self, nvidia_temp, nvidia_mem, nvidia_clock, nvidia_watts, nvidia_fan):
        self.gpu_temp_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_temp_label.setText(" %d C" % nvidia_temp)
        self.gpu_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_mem_label.setText("%d" % nvidia_mem)
        self.gpu_clock_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_clock_label.setText("%d" % nvidia_clock)
        self.gpu_watts_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_watts_label.setText("%d" % nvidia_watts)
        self.gpu_fan_progressbar.setValue(nvidia_fan)

    def choose_kill_process(self):
        row = self.process_table_widget.currentItem().row()
        column = self.process_table_widget.currentItem().column()
        cell = self.process_table_widget.item(row, column).text()
        return cell

    def kill_process(self):
        killall = "killall %s" % self.choose_kill_process()
        subprocess.check_output(killall, shell=True)


if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    app = MainClass()
    app.show()
    sys.exit(a.exec_())

