import psutil
import subprocess
import numpy as np
import cpuinfo




def list_cpus():
    total_cpu = psutil.cpu_count(logical=True)
    return total_cpu

def cpu_clock_speed():
    clock_speed = "cat /proc/cpuinfo | grep MHz | awk '{print $4}'"
    show_speed = subprocess.check_output(clock_speed, shell=True, universal_newlines=True).splitlines()
    return show_speed


def cpu_load_percentage():
        cpu_load = psutil.cpu_percent(percpu=False)
        show_cpu_load = np.array(cpu_load)
        return show_cpu_load


def total_cpu_percentage():
    cpu_load = psutil.cpu_percent(percpu=True)
    cpu_load = list(map(str, cpu_load))
    return cpu_load


def cpu_temp():
    find_cpu = cpuinfo.get_cpu_info()
    find_cpu_model = find_cpu.get("vendor_id")
    vm_find = "glxinfo | grep 'OpenGL vendor string:'"
    vm_list = subprocess.check_output(vm_find, shell=True, universal_newlines=True).strip()
    show_vm = repr(vm_list)
    if find_cpu_model == "AuthenticAMD":
        find_temp = 'sensors | grep Tdie: | cut -c 16-19'
        temp = subprocess.check_output(find_temp, shell=True, universal_newlines=True).strip()
        show_temp = repr(temp)
        if show_temp == repr(temp):
            return temp
        else:
            fx_temp = 'sensors | grep temp1: | cut -c 16-19'
            temp = subprocess.check_output(fx_temp, shell=True, universal_newlines=True).strip()
            return temp
    elif find_cpu_model == "GenuineIntel":
        intel_temperatures = "sensors | grep -E 'Core [0-99]' | cut -c 16-19"
        temp = subprocess.check_output(intel_temperatures, shell=True, universal_newlines=True).splitlines()
        temp_ints = np.array(temp)
        temp_update = temp_ints.astype(np.float)
        np.around(temp_update)
        temp =  sum(temp_update) / len(temp_update)
        return(str(temp))

def cpu_fan():
    find_cpu = cpuinfo.get_cpu_info()
    find_cpu_model = find_cpu.get("vendor_id")
    vm_find = "glxinfo | grep 'OpenGL vendor string:'"
    vm_list = subprocess.check_output(vm_find, shell=True, universal_newlines=True).strip()
    show_vm = repr(vm_list)
    if find_cpu_model == "AuthenticAMD":
        fan = "sensors | grep -m 1 fan | awk '{print $2}'"
        pass_cpu_fan = subprocess.check_output(fan, shell=True, universal_newlines=True).strip()
        show_cpu_fan = int(pass_cpu_fan)
        return show_cpu_fan
    elif find_cpu_model == "GenuineIntel":
        fan = "sensors | grep -m 1 fan | awk '{print $2}'"
        pass_cpu_fan = subprocess.check_output(fan, shell=True, universal_newlines=True).strip()
        fan_values = list(map(int, pass_cpu_fan))
        try:
            if fan_values[0] == 0:
                return fan_values[1]
        except:
            return 0

