import subprocess

def amdgpu_temp():
    temp_query = "cat /sys/kernel/debug/dri/0/amdgpu_pm_info | grep Temperature | awk '{print $3}'"
    temp = subprocess.check_output(temp_query, shell=True)
    temp = int(temp)
    return temp


def amdgpu_mem_speed():
    mem_speed_query = "cat /sys/kernel/debug/dri/0/amdgpu_pm_info | grep -m 1 MCLK | awk '{print $1}'"
    mem = subprocess.check_output(mem_speed_query, shell=True)
    mem = int(mem)
    return mem

def amdgpu_clock_speed():
    clock_speed_query =  "cat /sys/kernel/debug/dri/0/amdgpu_pm_info | grep -m 1 SCLK | awk '{print $1}'"
    clock = subprocess.check_output(clock_speed_query, shell=True)
    clock = int(clock)
    return clock

def amdgpu_watts():
    watts_query = "cat /sys/kernel/debug/dri/0/amdgpu_pm_info | grep -m 1 'W (average ' | awk '{print $1}'"
    watts = subprocess.check_output(watts_query, shell=True)
    watts = float(watts)
    int(watts)
    return watts

def amdgpu_fan():
    fan_speed = "cat /sys/class/drm/card0/device/hwmon/hwmon0/pwm1"
    max_fan = "cat /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_max"
    fan = subprocess.check_output(fan_speed, shell=True)
    max = subprocess.check_output(max_fan, shell=True)
    max = int(max)
    fan = int(fan)
    return fan / max * 100


def amdgpu_fan_max():
    max_fan = "cat /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_max"
    max = subprocess.check_output(max_fan, shell=True)
    max = int(max)
    return max