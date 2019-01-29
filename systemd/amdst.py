#!/usr/bin/env python3

import subprocess

permissions = "chmod -R a+rX /sys/kernel/debug"
subprocess.check_output(permissions, shell=True)
