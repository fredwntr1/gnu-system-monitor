from pynvml import *
import os
nvmlInit()
gpuObj = nvmlDeviceGetHandleByIndex(0)


def nvidia_temp():
    temperature = nvmlDeviceGetTemperature(gpuObj, NVML_TEMPERATURE_GPU)
    return temperature


def nvidia_clock():
    clock = nvmlDeviceGetClockInfo(gpuObj, NVML_CLOCK_GRAPHICS)

    return clock


def nvidia_mem():
    mem = nvmlDeviceGetClockInfo(gpuObj, NVML_CLOCK_MEM)
    return mem


def nvidia_voltage():
    voltage = nvmlDeviceGetPowerUsage(gpuObj)
    return voltage / 1000


def nvidia_fan_speed():
    fan = nvmlDeviceGetFanSpeed(gpuObj)
    return fan


def set_fan_speed():
    manual_fan = os.system("nvidia-settings -a [gpu:0]/GPUFanControlState=1")
    return manual_fan


