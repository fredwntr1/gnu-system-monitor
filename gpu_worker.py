from PyQt4 import QtCore
import time




class GpuWorker(QtCore.QThread):
    def __init__(self):
        super(GpuWorker, self).__init__()

    def run(self):
        import test
        while True:
            if test.find_gpu() == repr('OpenGL vendor string: NVIDIA Corporation'):
                import nvidia_gpu_stats
                nvidia_temp = nvidia_gpu_stats.nvidia_temp()
                nvidia_mem = nvidia_gpu_stats.nvidia_mem()
                nvidia_clock = nvidia_gpu_stats.nvidia_clock()
                nvidia_watts = nvidia_gpu_stats.nvidia_voltage()
                nvidia_fan = nvidia_gpu_stats.nvidia_fan_speed()
                self.emit(QtCore.SIGNAL("GPU_STATS"), nvidia_temp, nvidia_mem, nvidia_clock, nvidia_watts, nvidia_fan)
                time.sleep(3)
            elif test.find_gpu() == repr(' OpenGL vendor string: AMD'):
                temp = None
                break


