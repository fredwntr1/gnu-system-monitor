import subprocess
import netifaces


def net_procs():
    find_network = """ss -tnp | grep -i ESTAB | sort | awk -F '"' '$0=$2'"""
    show_network = subprocess.check_output(find_network, shell=True, universal_newlines=True).splitlines()
    return show_network


def net_proc_download():
    find_download = "ss -tnp | grep -i ESTAB | sort | awk '{print $2}'"
    show_download = subprocess.check_output(find_download, shell=True, universal_newlines=True).splitlines()
    download = list(map(str, show_download))
    return download


def net_proc_upload():
    find_upload = "ss -tnp | grep -i ESTAB | sort | awk '{print $3}'"
    show_upload = subprocess.check_output(find_upload, shell=True, universal_newlines=True).splitlines()
    upload = list(map(str, show_upload))
    return upload




