import subprocess


find_stats = str(subprocess.check_output("$PWD/gpu_stats.sh", shell=True, universal_newlines=True)).strip()
find_stats_add = ["cat", "amdgpu_pm_info"]
find_stats_query = "%s %s/%s" %(find_stats_add[0], find_stats, find_stats_add[1])
show_stats = subprocess.check_output(find_stats_query, shell=True).strip()


def amdgpu_temp():
    t = ["| grep Temperature", "| awk '{print $3}'"]
    temp_query = "%s %s %s" %(find_stats_query, t[0], t[1])
    temp = int(subprocess.check_output(temp_query, shell=True, universal_newlines=True))
    return temp


def amdgpu_mem_speed():
    m = ["| grep -m 1 MCLK", "| awk '{print $1}'"]
    mem_query = "%s %s %s" %(find_stats_query, m[0], m[1])
    mem = int(subprocess.check_output(mem_query, shell=True))
    return mem


def amdgpu_clock_speed():
    c = ["| grep -m 1 SCLK", "| awk '{print $1}'"]
    clock_query = "%s %s %s" %(find_stats_query, c[0], c[1])
    clock = int(subprocess.check_output(clock_query, shell=True))
    return clock


def amdgpu_watts():
    w = ["| grep -m1 'W (average '", "| awk '{print $1}'"]
    watts_query = "%s %s %s" %(find_stats_query, w[0], w[1])
    watts = float(subprocess.check_output(watts_query, shell=True))
    int(watts)
    return watts

def amdgpu_fan_max():
    fan_find = str(subprocess.check_output("$PWD/find_gpus.sh", shell=True, universal_newlines=True)).strip()
    fan_max_add = ["cat", "pwm1_max"]
    fan_max_query = "%s  %s/%s" % (fan_max_add[0], fan_find, fan_max_add[1])
    show_max_fan = int(subprocess.check_output(fan_max_query, shell=True))
    return show_max_fan

def amdgpu_fan():
    fan_find = str(subprocess.check_output("$PWD/find_gpus.sh", shell=True, universal_newlines=True)).strip()
    fan_add = ["cat", "pwm1"]
    fan_add_query = "%s  %s/%s" %(fan_add[0], fan_find, fan_add[1])
    fan = int(subprocess.check_output(fan_add_query, shell=True))
    max = amdgpu_fan_max()
    return fan / max * 100

def enable_manual_fan():
    fan_find = str(subprocess.check_output("$PWD/find_gpus.sh", shell=True, universal_newlines=True)).strip()
    state = ["echo -n '1' > ", "pwm1_enable"]
    state_add = "%s %s/%s" %(state[0], fan_find, state[1])
    enable = subprocess.check_output(state_add, shell=True)
    return enable

def disable_manual_fan():
    fan_find = str(subprocess.check_output("$PWD/find_gpus.sh", shell=True, universal_newlines=True)).strip()
    state = ["echo -n '2' > ", "pwm1_enable"]
    state_add = "%s %s/%s" % (state[0], fan_find, state[1])
    disable = subprocess.check_output(state_add, shell=True)
    return disable

def fan_value():
    fan_find = str(subprocess.check_output("$PWD/find_gpus.sh", shell=True, universal_newlines=True)).strip()
    state = ["echo -n '%d' > ", "pwm1"]
    state_add = "%s %s/%s" % (state[0], fan_find, state[1])
    return state_add

