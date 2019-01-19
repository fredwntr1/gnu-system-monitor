#!/usr/bin/env python3
import sys
from PyQt4 import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import ui
import mem_worker
import cpu_worker
import gpu_worker
import net_worker
import subprocess
import time


class MainClass(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainClass, self).__init__()
        self.setupUi(self)
        self.mem_stats = mem_worker.MemStats()
        self.mem_table = mem_worker.MemProcessTableWorker()
        self.cpu_worker = cpu_worker.CpuWorker()
        self.gpu_stats = gpu_worker.GpuStats()
        self.net_worker = net_worker.NetProcessWorker()
        self.cpu_table = cpu_worker.CpuTable()
        self.mem_graph_worker = mem_worker.MemGraphWorker()
        self.mem_graph_worker.start()
        self.cpu_graph_worker = cpu_worker.CpuGraphWorker()
        self.cpu_graph_worker.start()
        self.cpu_table.start()
        self.mem_stats.start()
        self.cpu_worker.start()
        self.gpu_stats.start()
        self.mem_table.start()
        self.net_worker.start()
        self.connect(self.mem_stats, QtCore.SIGNAL("MEM_STATS"), self.show_mem_stats)
        self.connect(self.cpu_worker, QtCore.SIGNAL("CPU_STATS"), self.show_cpu_stats)
        self.connect(self.gpu_stats, QtCore.SIGNAL("GPU_STATS"), self.show_gpu_stats)
        self.connect(self.mem_table, QtCore.SIGNAL('UPDATE_MEM_PROCS'), self.update_process_table)
        self.connect(self.net_worker, QtCore.SIGNAL("NET_STATS"), self.show_net_stats)
        self.connect(self.cpu_table, QtCore.SIGNAL("CPU_TABLE"), self.update_cpu_table)
        self.connect(self.mem_graph_worker, QtCore.SIGNAL("UPDATE_MEM_GRAPH"), self.update_mem_graph)
        self.connect(self.cpu_graph_worker, QtCore.SIGNAL("CPU_GRAPH"), self.update_cpu_graph)
        self.process_table_widget.cellClicked.connect(self.choose_kill_process)
        self.end_task_pushbutton.clicked.connect(self.kill_process)
        self.net_limit_pushbutton.setEnabled(False)
        self.gpu_fan_slider.valueChanged.connect(self.change_fan_speed)
        self.gpu_cfan_checkbox.toggled.connect(self.enable_manual_fanspeed)
        self.gpu_oc_checkbox.toggled.connect(self.oc_performance_level)
        self.gpu_performance_radio.toggled.connect(self.oc_performance_level)
        self.gpu_adaptive_radio.toggled.connect(self.oc_performance_level)
        self.gpu_mem_sliderbar.valueChanged.connect(self.enable_gpu_mem_overclock)
        self.gpu_clock_sliderbar.valueChanged.connect(self.enable_gpu_core_oc)
        self.gpu_watts_sliderbar.valueChanged.connect(self.enable_gpu_watts_oc)
        self.gpu_adaptive_radio.setEnabled(False)
        self.gpu_performance_radio.setEnabled(False)
        self.gpu_watts_sliderbar.setEnabled(False)
        self.gpu_clock_sliderbar.setEnabled(False)
        self.gpu_mem_sliderbar.setEnabled(False)
        self.gpu_fan_slider.setEnabled(False)

    def update_cpu_graph(self, core_count, cpu_load):
        cores = []
        load = np.array(cpu_load)
        flload = load.astype(float)
        for x in (range(core_count)):
            x = "CPU: " + str(x)
            cores.append(x)
        x2dict = dict(enumerate(cores))
        self.cpu_graph_widget.getAxis('bottom').setTicks([x2dict.items()])
        x1 = np.arange(len(cores))
        y1 = flload.tolist()
        self.cpu_graph_widget.setLabel('left', '<span style="color: white">Cpu Load</span>', units='%')
        self.cpu_graph_widget.setXRange(0, len(cores), padding=0.1)
        self.cpu_graph_widget.setYRange(0, 100, padding=0)
        c1 = pg.BarGraphItem(x=x1, height=y1, width=0.2)
        self.cpu_graph_widget.addItem(c1)

    def update_mem_graph(self, used_mem, free_mem, used_swap):
        ticks = ["used", "free", "swap"]
        xdict = dict(enumerate(ticks))
        y1 = [used_mem, free_mem, used_swap]
        x1 = np.arange(3)
        self.process_mem_graph.getAxis('bottom').setTicks([xdict.items()])
        self.process_mem_graph.setLabel('left', '<span style="color: white">Memory</span>', units='%')
        self.process_mem_graph.setYRange(0, 100, padding=0.1)
        self.process_mem_graph.setXRange(0, 3, padding=0.2)
        p1 = pg.BarGraphItem(x=x1, height=y1, width=0.3)
        self.process_mem_graph.addItem(p1)

    def mem_usage_graph(self):
        import mem_stats
        free_mem_plot = mem_stats.free_mem()
        while True:
            self.process_mem_graph.plotItem(free_mem_plot)
            time.sleep(2)

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

    def show_cpu_stats(self, cpu_percent, temp, fan):
        self.cpu_fan_speed_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.cpu_fan_speed_label.setText("%d RPM" % fan)
        self.cpu_temp_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.cpu_load_progressbar.setValue(cpu_percent)
        self.cpu_temp_label.setText("   %s C" % temp)

    def show_gpu_stats(self, nvidia_temp, nvidia_mem, nvidia_clock, nvidia_watts, nvidia_fan):
        self.gpu_temp_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_temp_label.setText(" %d C" % nvidia_temp)
        self.gpu_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_mem_label.setText("%d" % nvidia_mem)
        self.gpu_clock_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_clock_label.setText("%d" % nvidia_clock)
        self.gpu_watts_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_watts_label.setText("%d W" % nvidia_watts)
        self.gpu_fan_progressbar.setValue(nvidia_fan)

    def update_cpu_table(self, cpu_freq, core_count, cpu_percent):
        self.cpu_table_widget.setColumnCount(core_count)
        cpu_list = []
        for x in (range(core_count)):
            self.cpu_header.setResizeMode(x, QtGui.QHeaderView.Stretch)
            x = "CPU: " + str(x)
            cpu_list.append(str(x))
        self.cpu_table_widget.setHorizontalHeaderLabels(cpu_list)
        for i, column in enumerate(cpu_freq):
            self.cpu_table_widget.setItem(0, i, QtGui.QTableWidgetItem(column))
        for i, column in enumerate(cpu_percent):
            self.cpu_table_widget.setItem(1, i, QtGui.QTableWidgetItem(column))

    def choose_kill_process(self):
        row = self.process_table_widget.currentItem().row()
        column = self.process_table_widget.currentItem().column()
        cell = self.process_table_widget.item(row, column).text()
        return cell

    def kill_process(self):
        killall = "killall %s" % self.choose_kill_process()
        subprocess.check_output(killall, shell=True)

    def change_fan_speed(self):
        self.gpu_fan_slider.setMinimum(0)
        self.gpu_fan_slider.setMaximum(100)
        fanspeed = self.gpu_fan_slider.value()
        speed = "nvidia-settings -a [fan-0]/GPUTargetFanSpeed=%d" % fanspeed
        set_speed = subprocess.check_output(speed, shell=True)
        return set_speed

    def enable_manual_fanspeed(self):
        manual = "nvidia-settings -a [gpu:0]/GPUFanControlState=1"
        auto = "nvidia-settings -a [gpu:0]/GPUFanControlState=0"
        if self.gpu_cfan_checkbox.isChecked():
            subprocess.check_output(manual, shell=True)
            self.gpu_fan_slider.setEnabled(True)
        else:
            self.gpu_fan_slider.setValue(0)
            subprocess.check_output(auto, shell=True)
            self.gpu_fan_slider.setEnabled(False)

    def oc_performance_level(self):

        if self.gpu_oc_checkbox.checkState() == QtCore.Qt.Checked:
            self.gpu_mem_sliderbar.setEnabled(True)
            self.gpu_clock_sliderbar.setEnabled(True)
            self.gpu_watts_sliderbar.setEnabled(True)
            self.gpu_adaptive_radio.setEnabled(True)
            self.gpu_performance_radio.setEnabled(True)
        elif self.gpu_oc_checkbox.checkState() != QtCore.Qt.Checked:
            self.gpu_clock_sliderbar.setValue(0)
            self.gpu_mem_sliderbar.setValue(0)
            self.gpu_watts_sliderbar.setValue(0)
            self.gpu_performance_radio.setEnabled(False)
            self.gpu_adaptive_radio.setEnabled(False)
            self.gpu_watts_sliderbar.setEnabled(False)
            self.gpu_clock_sliderbar.setEnabled(False)
            self.gpu_mem_sliderbar.setEnabled(False)
        if self.gpu_adaptive_radio.isChecked():
            self.gpu_performance_radio.setChecked(False)
        elif self.gpu_performance_radio.isChecked():
            self.gpu_adaptive_radio.setChecked(False)

    def enable_gpu_mem_overclock(self):
        adaptive = 2
        performance = 3
        mem_value = self.gpu_mem_sliderbar.value()
        adaptive_mem = "nvidia-settings -a [gpu:0]/GPUMemoryTransferRateOffset[%d]=%d" % (adaptive, mem_value)
        performance_mem = "nvidia-settings -a [gpu:0]/GPUMemoryTransferRateOffset[%d]=%d" % (performance, mem_value)
        clear_mem_oc = "nvidia-settings -a [gpu:0]/GPUMemoryTransferRateOffset[3]=0"
        self.gpu_mem_sliderbar.setMinimum(0)
        self.gpu_mem_sliderbar.setMaximum(2000)
        if self.gpu_oc_checkbox.isChecked() and self.gpu_adaptive_radio.isChecked():
            show_mem = subprocess.check_output(adaptive_mem, shell=True)
            return show_mem
        elif self.gpu_oc_checkbox.isChecked() and self.gpu_performance_radio.isChecked():
            show_mem = subprocess.check_output(performance_mem, shell=True)
            return show_mem
        elif self.gpu_oc_checkbox.checkState() != QtCore.Qt.Checked:
            clear = subprocess.check_output(clear_mem_oc, shell=True)
            return clear

    def enable_gpu_core_oc(self):
        adaptive = 2
        performance = 3
        clock_value = self.gpu_clock_sliderbar.value()
        adaptive_clock = "nvidia-settings -a [gpu:0]/GPUGraphicsClockOffset[%d]=%d" % (adaptive, clock_value)
        performance_clock = "nvidia-settings -a [gpu:0]/GPUGraphicsClockOffset[%d]=%d" % (performance, clock_value)
        clear_clock = "nvidia-settings -a [gpu:0]/GPUGraphicsClockOffset[3]=0"
        self.gpu_clock_sliderbar.setMinimum(0)
        self.gpu_clock_sliderbar.setMaximum(800)
        if self.gpu_oc_checkbox.isChecked() and self.gpu_adaptive_radio.isChecked():
            show_clock = subprocess.check_output(adaptive_clock, shell=True)
            return show_clock
        elif self.gpu_oc_checkbox.isChecked() and self.gpu_performance_radio.isChecked():
            show_clock = subprocess.check_output(performance_clock, shell=True)
            return show_clock
        elif self.gpu_oc_checkbox.checkState() != QtCore.Qt.Checked:
            clear = subprocess.check_output(clear_clock, shell=True)
            return clear

    def enable_gpu_watts_oc(self):
        adaptive = 2
        performance = 3
        watts_value = self.gpu_watts_sliderbar.value()
        adaptive_watts = "nvidia-settings -a [gpu:0]/GPUOverVoltageOffset[%d]=%d" % (adaptive, watts_value)
        performance_watts = "nvidia-settings -a [gpu:0]/GPUOverVoltageOffset[%d]=%d" % (performance, watts_value)
        clear_watts_oc = "nvidia-settings -a [gpu:0]/GPUOverVoltageOffset[3]=0"
        self.gpu_watts_sliderbar.setMinimum(0)
        self.gpu_watts_sliderbar.setMaximum(30)
        if self.gpu_oc_checkbox.isChecked() and self.gpu_adaptive_radio.isChecked():
            show_watts = subprocess.check_output(adaptive_watts, shell=True)
            return show_watts
        elif self.gpu_oc_checkbox.isChecked() and self.gpu_performance_radio.isChecked():
            show_watts = subprocess.check_output(performance_watts, shell=True)
            return show_watts
        elif self.gpu_oc_checkbox.checkState() != QtCore.Qt.Checked:
            clear = subprocess.check_output(clear_watts_oc, shell=True)
            return clear


if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    app = MainClass()
    app.show()
    sys.exit(a.exec_())

