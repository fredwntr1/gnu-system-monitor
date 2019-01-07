import psutil
import subprocess
import numpy as np


# list number of cpu cores as well as logical cores so far this function is unused
def list_cpus():
    total_cpu = psutil.cpu_count(logical=True)
    return total_cpu


def cpu_load_percentage():
        cpu_load = psutil.cpu_percent(percpu=False)
        show_cpu_load = np.array(cpu_load)
        return show_cpu_load


def cpu_fan_rpm():
    cpu_fan = 'sensors | grep -m 1 fan | cut -c 24-28'
    pass_cpu_fan = subprocess.check_output(cpu_fan, shell=True, universal_newlines=True).strip()
    show_cpu_fan = int(pass_cpu_fan)
    return show_cpu_fan


# Figures out which cpu vendor you are using
def find_cpu():
    cpu_type = "lscpu | grep 'Model name:' | cut -c 22-24"
    find_cpu_model = subprocess.check_output(cpu_type, shell=True, universal_newlines=True).strip()
    show_cpu_model = repr(find_cpu_model)
    return show_cpu_model


def amd_temp():
    amd_ryzen_temp = 'sensors | grep Tdie: | cut -c 16-19'
    temp = subprocess.check_output(amd_ryzen_temp, shell=True, universal_newlines=True).strip()
    show_temp = repr(temp)
    if show_temp == repr(temp):
        return temp
    else:
        amd_fx_temp = 'sensors | grep temp1: | cut -c 16-19'
        temp = subprocess.check_output(amd_fx_temp, shell=True, universal_newlines=True ).strip()
        return temp


def intel_temp():
    intel_temperatures = "sensors | grep -E 'Core [0-99]' | cut -c 16-19"
    temp = subprocess.check_output(intel_temperatures, shell=True, universal_newlines=True).splitlines()
    temp_ints = np.array(temp)
    temp_update = temp_ints.astype(np.float)
    return sum(temp_update) / len(temp_update)

