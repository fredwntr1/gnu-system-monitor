import psutil
import subprocess


def mem_procs():
    proc_name = """ps -eo user,comm,%mem,%cpu,pid | grep -i "$USER" | awk '{print $2}'"""
    show_proc_name = subprocess.check_output(proc_name, shell=True, universal_newlines=True).splitlines()
    return show_proc_name


def user_proc():
    find_user = """ps -eo user,comm,%mem,%cpu,pid | grep -i "$USER" | awk '{print $1}'"""
    show_user_proc = subprocess.check_output(find_user, shell=True, universal_newlines=True).splitlines()
    return show_user_proc


def proc_cpu_percent():
    find_cpu_percent = """ps -eo user,comm,%mem,%cpu,pid | grep -i "$USER"| awk '{print $4}'"""
    show_cpu_percent = subprocess.check_output(find_cpu_percent, shell=True, universal_newlines=True).splitlines()
    return show_cpu_percent


def proc_mem_percent():
    find_mem_percent = """ps -eo user,comm,%mem,%cpu,pid | grep -i "$USER" | awk '{print $3}'"""
    show_mem_percent = subprocess.check_output(find_mem_percent, shell=True, universal_newlines=True).splitlines()
    return show_mem_percent


def proc_pids():
    find_pid = """ps -eo user,comm,%mem,%cpu,pid | grep -i "$USER" | awk '{print $5}'"""
    show_pid = subprocess.check_output(find_pid, shell=True, universal_newlines=True).splitlines()
    return show_pid


def total_swap_mem():
    find_swap = psutil.swap_memory()
    total_swap = find_swap.total / 1000000
    return round(total_swap)


def used_swap_mem():
    find_swap = psutil.swap_memory()
    used_swap = find_swap.used / 1000000
    return round(used_swap)


def total_mem():
    find_total_mem = psutil.virtual_memory()
    total_memory = find_total_mem.total / 1000000
    return round(total_memory)


def free_mem():
    find_free_mem = psutil.virtual_memory()
    free_mem = find_free_mem.available / 1000000
    return round(free_mem)

