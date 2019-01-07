
import subprocess
import numpy as np
import psutil

# Decide whether or not it's a ryzen or fx cpu.
def find_gpu():
    gpu_type = "glxinfo | grep 'OpenGL vendor string:'"
    find_gpu_vendor = subprocess.check_output(gpu_type, shell=True, universal_newlines=True).strip()
    show_gpu_vendor = repr(find_gpu_vendor)
    return show_gpu_vendor


def nvidia_temp():
    temp = "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader"
    process_temp = subprocess.check_output(temp, shell=True, universal_newlines=True).strip()
    show_temp = int(process_temp)
    return show_temp


