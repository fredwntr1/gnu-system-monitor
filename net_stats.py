import subprocess
import netifaces


def net_procs():
    find_network = "netstat -tnp | grep -i stab | awk -F/ '{print $2}' | sort | uniq"
    show_network = subprocess.check_output(find_network, shell=True, universal_newlines=True).splitlines()
    return show_network


def net_proc_download():
    find_download = "netstat -tnp | grep -i tcp | awk '{print $2}' | sort | uniq"
    show_download = subprocess.check_output(find_download, shell=True, universal_newlines=True).splitlines()
    download = list(map(str, show_download))
    return download


def net_proc_upload():
    find_upload = "netstat -tnp | grep -i tcp | awk '{print $3}' | sort | uniq"
    show_upload = subprocess.check_output(find_upload, shell=True, universal_newlines=True).splitlines()
  #  show_upload.remove("Send-Q")
    upload = list(map(str, show_upload))
    return upload




#net_proc_download()