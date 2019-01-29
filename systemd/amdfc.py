#!/usr/bin/env python3

import os

os.system("find / -type f -name 'pwm1*' -exec chmod 777 {} \;")
