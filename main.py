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
        self.gpu_fan_speed_slider.hide()
        self.gpu_clock_slider.hide()
        self.gpu_mem_slider.hide()
        self.gpu_watts_slider.hide()
        self.adaptive_oc_radio.hide()
        self.performance_oc_radio.hide()
        self.manual_fanspeed_checkbox.toggled.connect(self.gpu_fan_bar)
        self.manual_overclocking_checkbox.toggled.connect(self.overclocking_bar)
        self.process_table_widget.cellClicked.connect(self.choose_kill_process)
        self.end_process_pushbutton.clicked.connect(self.kill_process)







    def show_net_stats(self, net_processes, net_download, net_upload):
        self.network_table_widget.setRowCount(len(net_processes))

        for i, row in enumerate(net_processes):
            self.network_table_widget.setItem(i, 0, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(net_download):
            self.network_table_widget.setItem(i, 1, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(net_upload):
            self.network_table_widget.setItem(i, 2, QtGui.QTableWidgetItem(row))

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

    def overclocking_bar(self):
        if self.manual_overclocking_checkbox.isChecked():
            self.gpu_clock_slider.show()
            self.gpu_mem_slider.show()
            self.gpu_watts_slider.show()
            self.adaptive_oc_radio.show()
            self.performance_oc_radio.show()
        else:
            self.gpu_clock_slider.hide()
            self.gpu_mem_slider.hide()
            self.gpu_watts_slider.hide()
            self.adaptive_oc_radio.hide()
            self.performance_oc_radio.hide()

    def gpu_fan_bar(self):
        if self.manual_fanspeed_checkbox.isChecked():
            self.gpu_fan_speed_slider.show()
        else:
            self.gpu_fan_speed_slider.hide()


    def show_mem_stats(self, free_mem, total_mem, total_swap_mem, used_swap_mem):
        self.free_memory_lcd.display(free_mem)
        self.total_memory_lcd.display(total_mem)
        self.total_swap_lcd.display(total_swap_mem)
        self.free_swap_lcd.display(used_swap_mem)

    def show_cpu_stats(self, cpu_fan, cpu_percent, cpu_temp):
        self.cpu_fan_speed_lcd.display(cpu_fan)
        self.cpu_load_progressbar.setValue(cpu_percent)
        self.cpu_temp_lcd.display(cpu_temp)

    def show_gpu_stats(self, nvidia_temp, nvidia_mem, nvidia_clock, nvidia_watts, nvidia_fan):
        self.gpu_temp_lcd.display(nvidia_temp)
        self.gpu_mem_lcd.display(nvidia_mem)
        self.gpu_clock_lcd.display(nvidia_clock)
        self.gpu_watts_lcd.display(nvidia_watts)
        self.gpu_fan_speed_progressbar.setValue(nvidia_fan)

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