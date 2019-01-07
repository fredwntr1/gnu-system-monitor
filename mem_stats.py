from __future__ import  print_function
import sys
import psutil
import numpy as np
from pprint import pprint as pp
import getpass
import collections

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


def mem_procs():
    pid = process_names = [proc.name() for proc in psutil.process_iter()]
    show_pid = np.array(pid)
    return show_pid


def user_proc():
    find_user = process_names = [proc.username() for proc in psutil.process_iter()]
    show_user = np.array(find_user)
    return show_user



def proc_cpu_percent():
    find_cpu_percent = process_names = [proc.cpu_percent() for proc in psutil.process_iter()]
    show_cpu_percent = np.array(find_cpu_percent)
    display_cpu_percent = list(map(str, show_cpu_percent))
    return display_cpu_percent

def proc_mem_percent():
    find_mem_percent = process_names = [proc.memory_percent() for proc in psutil.process_iter()]
    show_mem_percent = np.array(find_mem_percent)
    round_mem_percent = np.around(show_mem_percent)
    display_mem_percent = list(map(str, round_mem_percent))
    return display_mem_percent


def proc_pids():
    find_pid = psutil.pids()
    show_pid = np.array(find_pid)
    display_pid = list(map(str, show_pid))
    return display_pid

