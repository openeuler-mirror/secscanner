# -*- coding: utf-8 -*-
'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''

import subprocess
from collections import Counter
import logging
import re
logger = logging.getLogger('secscanner')


def get_ip_login_counts():
    # Execute the last command and obtain the output
    last_output = subprocess.check_output("last", shell=True)

    # Using regular expressions to match IP addresses
    ip_pattern = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$')

    # Initialize counter
    ip_counts = Counter()
    lines = last_output.decode('utf-8').strip().split('\n')

    for line in lines:
        fields = line.split()
        if len(fields) >= 3:
            ip = fields[2]
            if ip_pattern.match(ip):
                # add number of ip
                ip_counts[ip] += 1
    # Returns a dictionary of IP addresses and their login attempts
    return ip_counts

if __name__ == '__main__':
    ip_counts = get_ip_login_counts()
    for ip, count in ip_counts.items():
        if count == 1:
            print(f"IP - {ip} Alarm prompt for first login of this IP !!")
