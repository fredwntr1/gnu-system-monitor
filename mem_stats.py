import psutil
import numpy as np

## mem_proc() function variables
process_name = process_names = [proc.name() for proc in psutil.process_iter()]
show_name = np.array(process_name)




## user_proc() function variables
find_user = process_names = [proc.username() for proc in psutil.process_iter()]
show_user = np.array(find_user)

## proc_cpu_percent() function variables
find_cpu_percent = process_names = [proc.cpu_percent() for proc in psutil.process_iter()]
show_cpu_percent = np.array(find_cpu_percent)
sort_cpu_percent = show_cpu_percent.argsort()

## proc_mem_percent() function variables
find_mem_percent = process_names = [proc.memory_percent() for proc in psutil.process_iter()]
show_mem_percent = np.array(find_mem_percent)
round_mem_percent = np.around(show_mem_percent)


## proc_pids() function variables
find_pid = psutil.pids()
show_pid = np.array(find_pid)


def mem_procs():
    sort_name = show_name[sort_cpu_percent]
    return list(map(str, sort_name))


def user_proc():
    sort_user = show_user[sort_cpu_percent]
    return list(map(str, sort_user))


def proc_cpu_percent():
    return list(map(str, sort_cpu_percent))


def proc_mem_percent():
    sort_mem = round_mem_percent[sort_cpu_percent]
    return list(map(str, round_mem_percent))


def proc_pids():
    display_pid = show_pid[sort_cpu_percent]
    return list(map(str, display_pid))

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


