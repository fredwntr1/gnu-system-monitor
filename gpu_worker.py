from PyQt4 import QtCore
import time
import subprocess
import multiprocessing


class GpuWorkerThreads(QtCore.QObject):
    gpu_stats_thread = QtCore.pyqtSignal(int, int, int, int, int)
    fan_curve_thread = QtCore.pyqtSignal(int, str, str, int)
    p3 = multiprocessing.Pool(processes=1)


class GpuStats(QtCore.QThread):
    def __init__(self):
        super(GpuStats, self).__init__()
        self.stats_signal = GpuWorkerThreads()

    def run(self):
        gpu_type = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
        find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        while True:
            if show_gpu_vendor  == repr('GeForce'):
                import nvidia_gpu_stats
                temp = self.stats_signal.p3.apply(nvidia_gpu_stats.nvidia_temp)
                mem = self.stats_signal.p3.apply(nvidia_gpu_stats.nvidia_mem)
                clock = self.stats_signal.p3.apply(nvidia_gpu_stats.nvidia_clock)
                watts = self.stats_signal.p3.apply(nvidia_gpu_stats.nvidia_voltage)
                fan = self.stats_signal.p3.apply(nvidia_gpu_stats.nvidia_fan_speed)
                self.stats_signal.gpu_stats_thread.emit(temp, mem, clock, watts, fan)
                QtCore.QCoreApplication.processEvents()
                time.sleep(1)
            elif show_gpu_vendor == repr('AMD'):
                import amdgpu
                temp = self.stats_signal.p3.apply(amdgpu.amdgpu_temp)
                mem = self.stats_signal.p3.apply(amdgpu.amdgpu_mem_speed)
                clock = self.stats_signal.p3.apply(amdgpu.amdgpu_clock_speed)
                watts = self.stats_signal.p3.apply(amdgpu.amdgpu_watts)
                fan = self.stats_signal.p3.apply(amdgpu.amdgpu_fan)
                self.stats_signal.gpu_stats_thread.emit(temp, mem, clock, watts, fan)
                QtCore.QCoreApplication.processEvents()
                time.sleep(1)


class GpuFanCurve(QtCore.QThread):
    def __init__(self):
        super(GpuFanCurve, self).__init__()
        self.fcurve_signal = GpuWorkerThreads()

    def run(self):
        gpu_type = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
        find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        while True:
            if show_gpu_vendor == repr('GeForce'):
                import nvidia_gpu_stats
                gpu_temp = self.fcurve_signal.p3.apply(nvidia_gpu_stats.nvidia_temp)
                max_fan = 100
                speed = "nvidia-settings -a [fan-0]/GPUTargetFanSpeed=%d"
                self.fcurve_signal.fan_curve_thread.emit(gpu_temp, speed, show_gpu_vendor, max_fan)
                QtCore.QCoreApplication.processEvents()
                time.sleep(3)
            elif show_gpu_vendor == repr('AMD'):
                import amdgpu
                gpu_temp = self.fcurve_signal.p3.apply(amdgpu.amdgpu_temp)
                max_fan = self.fcurve_signal.p3.apply(amdgpu.amdgpu_fan_max)
                speed = self.fcurve_signal.p3.apply(amdgpu.fan_value)
                self.fcurve_signal.fan_curve_thread.emit(gpu_temp, speed, show_gpu_vendor, max_fan)
                QtCore.QCoreApplication.processEvents()
                time.sleep(1)


