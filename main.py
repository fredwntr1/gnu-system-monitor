#!/usr/bin/env python3
from PyQt5 import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import ui
import mem_worker
import cpu_worker
import gpu_worker
import net_worker
import subprocess
import sys


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [QtCore.QTime().addMSecs(value).toString('mm:ss') for value in values]


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
        self.gpu_fancurve = gpu_worker.GpuFanCurve()
        self.cpu_timer = pg.QtCore.QTimer()
        self.cpu_timer.start(2000)
        self.memtime = pg.QtCore.QTime()
        self.memtime.start()
        self.cpu_graph_worker = cpu_worker.CpuGraphWorker()
        self.mem_stats.start()
        self.mem_table.start()
        self.mem_graph_worker.start()
        self.cpu_worker.start()
        self.cpu_table.start()
        self.cpu_graph_worker.start()
        self.gpu_stats.start()
        self.gpu_fancurve.start()
        self.net_worker.start()
        self.mem_stats.mem_worker_signal.mem_stats_signal.connect(self.show_mem_stats)
        self.mem_table.mem_worker_signal.mem_table_signal.connect(self.update_process_table)
        self.mem_graph_worker.mem_worker_signal.mem_graph_signal.connect(self.update_mem_graph)
        self.cpu_worker.stats_signal.cpu_worker_signal.connect(self.show_cpu_stats)
        self.cpu_graph_worker.graph_signal.cpu_graph_signal.connect(self.update_cpu_graph)
        self.cpu_table.table_signal.cpu_table_signal.connect(self.update_cpu_table)
        self.gpu_stats.stats_signal.gpu_stats_thread.connect(self.show_gpu_stats)
        self.gpu_fancurve.fcurve_signal.fan_curve_thread.connect(self.set_gpu_fancurve)
        self.net_worker.net_signal.net_proc_thread.connect(self.show_net_stats)
        self.cpu_timer.timeout.connect(self.refresh_graph_cpu)
        self.gpu_cfan_checkbox.toggled.connect(self.enable_manual_fanspeed)
        self.process_table_widget.cellClicked.connect(self.choose_kill_process)
        self.end_task_pushbutton.clicked.connect(self.kill_process)
        self.net_limit_pushbutton.setEnabled(False)
        self.gpu_fan_slider.valueChanged.connect(self.change_fan_speed)
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
        self.cpu_graph_widget.update()
        self.gpu_graph_widget.setEnabled(False)
        self.gpu_fcurve_checkbox.toggled.connect(self.enable_gpu_fancurve)
        self.p1 = pg.PolyLineROI([0, 0], closed=False, invertible=False, removable=True)
        self.gpu_graph_widget.addItem(self.p1)
        self.tab_widget.currentChanged.connect(self.set_gpu_tab)
        self.gpu_graph_widget.setMouseEnabled(x=False, y=False)
        self.cpu_graph_widget.setMouseEnabled(x=False, y=False)
        self.process_mem_graph.addLabel(text='Used Mem', angle=-90, color='r',)
        self.process_mem_graph.addLabel(text="Free Mem", angle=-90, color='b')
        self.process_mem_graph.addLabel(text='Used Swap', angle=-90, color='g')
        self.used_mem_plot = self.process_mem_graph.addPlot(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.mem_data1 = []
        self.mem_data2 = []
        self.mem_data3 = []
        self.mem_curve1 = self.used_mem_plot.plot()
        self.mem_curve2 = self.used_mem_plot.plot()
        self.mem_curve3 = self.used_mem_plot.plot()

    def set_gpu_tab(self):
        gpu_vendor = "glxinfo | grep 'OpenGL vendor string:'"
        find_gpu_vendor = subprocess.check_output(gpu_vendor, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        if show_gpu_vendor == repr("OpenGL vendor string: Intel Open Source Technology Center"):
            self.tab_widget.setTabEnabled(2, False)

    @QtCore.pyqtSlot(int, list)
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
        self.cpu_graph_widget.showGrid(x=True, y=True, alpha=0.3)
        c1 = pg.BarGraphItem(x=x1, height=y1, width=0.3, brush='b')
        self.cpu_graph_widget.addItem(c1)

    def refresh_graph_cpu(self):
        self.cpu_graph_widget.clear()
        QtCore.QCoreApplication.processEvents()

    @QtCore.pyqtSlot(int, int, int)
    def update_mem_graph(self, used_mem, free_mem, used_swap):
        self.mem_data1.append({'x': self.memtime.elapsed(), 'y': used_mem})
        self.mem_data2.append({'x': self.memtime.elapsed(), 'y': free_mem})
        self.mem_data3.append({'x': self.memtime.elapsed(), 'y': used_swap})

        x1 = [item['x'] for item in self.mem_data1]
        y1 = [item['y'] for item in self.mem_data1]
        x2 = [item['x'] for item in self.mem_data2]
        y2 = [item['y'] for item in self.mem_data2]
        x3 = [item['x'] for item in self.mem_data3]
        y3 = [item['y'] for item in self.mem_data3]

        self.mem_curve1.setData(x=x1, y=y1, pen='r')
        self.mem_curve2.setData(x=x2, y=y2, pen='b')
        self.mem_curve3.setData(x=x3, y=y3, pen='g')

    def refresh_graph_mem(self):
        self.process_mem_graph.clear()
        QtCore.QCoreApplication.processEvents()

    @QtCore.pyqtSlot(list, list, list)
    def show_net_stats(self, net_processes, net_download, net_upload):
        self.net_process_widget.setRowCount(len(net_processes))
        for i, row in enumerate(net_processes):
            self.net_process_widget.setItem(i, 0, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(net_download):
            self.net_process_widget.setItem(i, 1, QtGui.QTableWidgetItem(row))
        for i, row in enumerate(net_upload):
            self.net_process_widget.setItem(i, 2, QtGui.QTableWidgetItem(row))

    @QtCore.pyqtSlot(list, list, list, list, list)
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

    @QtCore.pyqtSlot(int, int, int)
    def show_mem_stats(self, free_mem, total_mem, total_swap_mem):
        self.free_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.free_mem_label.setText("   %d" % free_mem)
        self.total_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.total_mem_label.setText("   %d" % total_mem)
        self.swap_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.swap_mem_label.setText("   %d" % total_swap_mem)

    @QtCore.pyqtSlot(int, str, int)
    def show_cpu_stats(self, cpu_percent, temp, fan):
        self.cpu_fan_speed_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.cpu_fan_speed_label.setText("%d RPM" % fan)
        self.cpu_temp_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.cpu_load_progressbar.setValue(cpu_percent)
        self.cpu_temp_label.setText("   %s C" % temp)

    @QtCore.pyqtSlot(int, int, int, int, int)
    def show_gpu_stats(self, temp, mem, clock, watts, fan):
        self.gpu_temp_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_temp_label.setText(" %dc" % temp)
        self.gpu_mem_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_mem_label.setText("%d" % mem)
        self.gpu_clock_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_clock_label.setText("%d" % clock)
        self.gpu_watts_label.setFont(QtGui.QFont("Ubuntu", 16, QtGui.QFont.Bold))
        self.gpu_watts_label.setText("%dw" % watts)
        self.gpu_fan_progressbar.setValue(fan)

    @QtCore.pyqtSlot(list, int, list)
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
        import amdgpu
        max_amdgpu = amdgpu.amdgpu_fan_max()
        self.gpu_fan_slider.setMinimum(0)
        fanspeed = self.gpu_fan_slider.value()
        gpu_type = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
        find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        if show_gpu_vendor == repr('AMD'):
            self.gpu_fan_slider.setMaximum(max_amdgpu)
            speed = amdgpu.fan_value() % fanspeed
            set_speed = subprocess.check_output(speed, shell=True)
            return set_speed
        elif show_gpu_vendor == repr('GeForce'):
            self.gpu_fan_slider.setMaximum(100)
            speed = "nvidia-settings -a [fan-0]/GPUTargetFanSpeed=%d" % fanspeed
            set_speed = subprocess.check_output(speed, shell=True)
            return set_speed

    def enable_gpu_fancurve(self):
        import amdgpu
        enable = "nvidia-settings -a [gpu:0]/GPUFanControlState=1"
        cancel = "nvidia-settings -a [gpu:0]/GPUFanControlState=0"
        if self.gpu_fcurve_checkbox.isChecked():
            try:
                subprocess.check_output(enable, shell=True)
            except:
                  subprocess.check_output(amdgpu.enable_manual_fan(), shell=True)
            self.gpu_graph_widget.setEnabled(True)
            self.gpu_cfan_checkbox.setEnabled(False)
        else:
            try:
                subprocess.check_output(cancel, shell=True)
            except:
                subprocess.check_output(amdgpu.disable_manual_fan(), shell=True)
            self.gpu_graph_widget.setEnabled(False)
            self.gpu_cfan_checkbox.setEnabled(True)

    def enable_manual_fanspeed(self):
        import amdgpu
        manual = "nvidia-settings -a [gpu:0]/GPUFanControlState=1"
        auto = "nvidia-settings -a [gpu:0]/GPUFanControlState=0"
        if self.gpu_cfan_checkbox.isChecked():
            try:
                subprocess.check_output(manual, shell=True)
            except:
                subprocess.check_output(amdgpu.enable_manual_fan(), shell=True)
            self.gpu_fan_slider.setEnabled(True)
            self.gpu_fcurve_checkbox.setEnabled(False)
        else:
            try:
                subprocess.check_output(auto, shell=True)
            except:
                subprocess.check_output(amdgpu.disable_manual_fan(), shell=True)
            self.gpu_fan_slider.setEnabled(False)
            self.gpu_fcurve_checkbox.setEnabled(True)

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
            adaptive = "nvidia-settings -a [gpu:0]/GPUPowerMizerMode=0"
            subprocess.check_output(adaptive, shell=True)
        elif self.gpu_performance_radio.isChecked():
            self.gpu_adaptive_radio.setChecked(False)
            performance = "nvidia-settings -a [gpu:0]/GPUPowerMizerMode=1"
            subprocess.check_output(performance, shell=True)

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

    @QtCore.pyqtSlot(int, str, str, int)
    def set_gpu_fancurve(self, gpu_temp, speed, show_gpu_vendor, max_fan):
        self.gpu_graph_widget.setMouseTracking(False)
        points = self.p1.getLocalHandlePositions()
        tval = np.around([p[1].x() for p in points])
        pval = np.around(([p[1].y() for p in points]))
        fan_percent = list(map(int, pval))
        temp = list(map(int, tval))
        match_temp = min(temp, key=lambda x: abs(x - gpu_temp))
        match_percent = temp.index(match_temp)
        set_fan = fan_percent[match_percent]

        if self.gpu_fcurve_checkbox.checkState() == QtCore.Qt.Checked:
            if show_gpu_vendor == repr('AMD'):
                speed = speed % (max_fan * set_fan / 100)
                if gpu_temp >= match_temp:
                    subprocess.check_output(speed, shell=True)
            elif show_gpu_vendor == repr('GeForce'):
                if gpu_temp >= match_temp:
                    speed = speed % set_fan
                    subprocess.check_output(speed, shell=True)

        elif self.gpu_fcurve_checkbox.checkState() != QtCore.Qt.Checked:
            pass


if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    app = MainClass()
    a.processEvents()
    app.show()
    sys.exit(a.exec_())
