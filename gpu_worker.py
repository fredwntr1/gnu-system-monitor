from PyQt4 import QtCore
import time
import subprocess


class GpuStats(QtCore.QThread):
    def __init__(self):
        super(GpuStats, self).__init__()

    def run(self):
        gpu_type = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
        find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        while True:
            if show_gpu_vendor  == repr('GeForce'):
                import nvidia_gpu_stats
                temp = nvidia_gpu_stats.nvidia_temp()
                mem = nvidia_gpu_stats.nvidia_mem()
                clock = nvidia_gpu_stats.nvidia_clock()
                watts = nvidia_gpu_stats.nvidia_voltage()
                fan = nvidia_gpu_stats.nvidia_fan_speed()
                self.emit(QtCore.SIGNAL("GPU_STATS"), temp, mem, clock, watts, fan)
                time.sleep(1)
            elif show_gpu_vendor == repr('AMD'):
                import amdgpu
                temp = amdgpu.amdgpu_temp()
                mem = amdgpu.amdgpu_mem_speed()
                clock = amdgpu.amdgpu_clock_speed()
                watts = amdgpu.amdgpu_watts()
                fan = amdgpu.amdgpu_fan()
                self.emit(QtCore.SIGNAL("GPU_STATS"), temp, mem, clock, watts, fan)
                time.sleep(1)
            QtCore.QCoreApplication.processEvents()


class GpuFanCurve(QtCore.QThread):
    def __init__(self):
        super(GpuFanCurve, self).__init__()

    def run(self):
        gpu_type = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
        find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        while True:
            if show_gpu_vendor == repr('GeForce'):
                import nvidia_gpu_stats
                gpu_temp = nvidia_gpu_stats.nvidia_temp()
                max_fan = 100
                speed = "nvidia-settings -a [fan-0]/GPUTargetFanSpeed=%d"
                self.emit(QtCore.SIGNAL("GPU_FANCURVE"), gpu_temp, speed, show_gpu_vendor, max_fan)
                time.sleep(3)
                QtCore.QCoreApplication.processEvents()
            elif show_gpu_vendor == repr('AMD'):
                import amdgpu
                gpu_temp = amdgpu.amdgpu_temp()
                max_fan = amdgpu.amdgpu_fan_max()
                speed = "echo %d > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1 "
                cancel = "echo 2 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_enable"
                self.emit(QtCore.SIGNAL("GPU_FANCURVE"), gpu_temp, speed, show_gpu_vendor, max_fan)
                time.sleep(1)
                QtCore.QCoreApplication.processEvents()