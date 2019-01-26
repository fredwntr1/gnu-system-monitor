from PyQt4 import QtCore
import time
import subprocess


class GpuStats(QtCore.QThread):
    def __init__(self):
        super(GpuStats, self).__init__()

    def run(self):
        gpu_type = "glxinfo | grep 'OpenGL vendor string:'"
        find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
        show_gpu_vendor = repr(find_gpu_vendor)
        while True:
            if show_gpu_vendor  == repr('OpenGL vendor string: NVIDIA Corporation'):
                import nvidia_gpu_stats
                nvidia_temp = nvidia_gpu_stats.nvidia_temp()
                nvidia_mem = nvidia_gpu_stats.nvidia_mem()
                nvidia_clock = nvidia_gpu_stats.nvidia_clock()
                nvidia_watts = nvidia_gpu_stats.nvidia_voltage()
                nvidia_fan = nvidia_gpu_stats.nvidia_fan_speed()
                self.emit(QtCore.SIGNAL("GPU_STATS"), nvidia_temp, nvidia_mem, nvidia_clock, nvidia_watts, nvidia_fan)
                time.sleep(1)
            elif show_gpu_vendor == repr('OpenGL vendor string: AMD'):
                temp = None
                time.sleep(3)
            QtCore.QCoreApplication.processEvents()



