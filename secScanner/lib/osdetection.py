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


import platform
import subprocess
import os
import pathlib

# 获取系统信息
SYSTEM = platform.system()
RELEASE = platform.release()
MACHINE = platform.machine()
HOMEDIRS = ['/home', '/root']
OS_FULLNAME = platform.uname().release
# 初始化变量
global OS_NAME
OS_FULLNAME = ""
global OS_VERSION
FIND_BINARIES = ""
SYSCTL_READKEY = ""
# 根据不同的系统设置变量
if SYSTEM == "AIX":
    OS_NAME = "AIX"
    OS_FULLNAME = "AIX " + RELEASE
    OS_VERSION = subprocess.check_output(["oslevel"]).strip().decode()
    MACHINE = subprocess.check_output(["uname", "-p"]).strip().decode()
    HARDWARE = subprocess.check_output(["uname", "-M"]).strip().decode()
    FIND_BINARIES = "whereis -b"
elif SYSTEM == "Darwin":
    OS_NAME = "MacOS"
    OS_VERSION = platform.mac_ver()[0]
    OS_FULLNAME = platform.mac_ver()[1]
    if os.path.isfile("/usr/bin/sw_vers"):
        OS_NAME = subprocess.check_output(["/usr/bin/sw_vers", "-productName"]).strip().decode()
        OS_VERSION = subprocess.check_output(["/usr/bin/sw_vers", "-productVersion"]).strip().decode()
    else:
        OS_NAME = "Mac OS X"
        OS_VERSION = platform.mac_ver()[2]
    HARDWARE = MACHINE
    HOMEDIRS = ["/Users"]
    FIND_BINARIES = "whereis"
    OS_KERNELVERSION = platform.release()
    SYSCTL_READKEY = ""
elif SYSTEM == "DragonFly":
    OS_NAME = "DragonFly BSD"
    OS_FULLNAME = subprocess.check_output(["uname", "-s", "-r"]).strip().decode()
    OS_VERSION = RELEASE
    HARDWARE = MACHINE
    HOMEDIRS = ["/home", "/root"]
    FIND_BINARIES = "whereis -q -a -b"
    OS_KERNELVERSION = subprocess.check_output(["uname", "-i"]).strip().decode()
    SYSCTL_READKEY = "sysctl -n"
elif SYSTEM == "FreeBSD":
    OS_NAME = "FreeBSD"
    OS_FULLNAME = subprocess.check_output(["uname", "-s", "-r"]).strip().decode()
    OS_VERSION = RELEASE
    HARDWARE = MACHINE
    HOMEDIRS = ["/home", "/root"]
    FIND_BINARIES = "whereis -q -a -b"
    OS_KERNELVERSION = subprocess.check_output(["uname", "-i"]).strip().decode()
    SYSCTL_READKEY = "sysctl -n"

    # 检查是否为TrueOS
    if os.path.isfile("/etc/defaults/trueos"):
        OS_NAME = "TrueOS"
        print("Result: found TrueOS file, system is completely based on FreeBSD though. Only adjusting OS name.")
elif SYSTEM == "HP-UX":
    OS_NAME = "HP-UX"
    OS_FULLNAME = subprocess.check_output(["uname", "-s", "-r"]).strip().decode()
    OS_VERSION = RELEASE
    HARDWARE = MACHINE
    FIND_BINARIES = "whereis -b"
    SYSCTL_READKEY = ""

elif SYSTEM == "Linux":
    OS_NAME = "Linux"
    OS_FULLNAME = ""
    OS_VERSION = RELEASE
    LINUX_VERSION = subprocess.check_output(["uname", "-r"]).strip().decode()
    HARDWARE = MACHINE
    HOMEDIRS = ["/home"]
    FIND_BINARIES = "whereis -b"
    OS_KERNELVERSION_FULL = subprocess.check_output(["uname", "-r"]).strip().decode()
    OS_KERNELVERSION = OS_KERNELVERSION_FULL.split("-")[0]

    # 检查是否为Amazon
    if os.path.exists("/etc/system-release"):
        with open("/etc/system-release", "r") as f:
            lines = f.readlines()
        for line in lines:
            if "Amazon" in line:
                OS_REDHAT_OR_CLONE = 1
                OS_FULLNAME = line.strip()
                OS_VERSION = line.strip().split(" ")[-1]
                lINUX_VERSION = "Amazon"

    # 检查是否为Arch Linux
    if os.path.exists("/etc/arch-release"):
        OS_FULLNAME = "Arch Linux"
        OS_VERSION = "Unknown"
        LINUX_VERSION = "Arch Linux"
    # Chakra Linux
    if os.path.exists("/etc/chakra-release"):
        with open("/etc/chakra-release", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("Chakra"):
                OS_FULLNAME = line.strip()
                OS_VERSION = line.strip().split(" ")[-1]
                LINUX_VERSION = "Chakra Linux"

    # Cobalt
    if os.path.exists("/etc/cobalt-release"):
        with open("/etc/cobalt-release", "r") as f:
            OS_FULLNAME = f.read().strip()
# CPUBuilders Linux
if os.path.exists("/etc/cpub-release"):
    with open("/etc/cpub-release") as file:
        OS_FULLNAME = file.read().strip()

# Debian/Ubuntu (***) - Set first to Debian
if os.path.exists("/etc/debian_version"):
    with open("/etc/debian_version") as file:
        OS_VERSION = file.read().strip()
    OS_FULLNAME = f"Debian {OS_VERSION}"
    LINUX_VERSION = "Debian"

# /etc/lsb-release does not exist on Debian
if os.path.exists("/etc/debian_version") and os.path.exists("/etc/lsb-release"):
    with open("/etc/debian_version") as file:
        OS_VERSION = file.read().strip()
    with open("/etc/lsb-release") as file:
        LSB_RELEASE_DATA = file.read()

    FIND = [line.split("=")[1].strip('"') for line in LSB_RELEASE_DATA.split("\n") if line.startswith("DISTRIB_ID=")]
    FIND = FIND[0] if FIND else ""

    if FIND == "Ubuntu":
        OS_VERSION = [line.split("=")[1].strip() for line in LSB_RELEASE_DATA.split("\n") if line.startswith("DISTRIB_RELEASE=")]
        OS_VERSION = OS_VERSION[0] if OS_VERSION else ""
        OS_FULLNAME = f"Ubuntu {OS_VERSION}"
        LINUX_VERSION = "Ubuntu"
    elif FIND == "elementary OS":
        LINUX_VERSION = "elementary OS"
        OS_VERSION = [line.split("=")[1].strip() for line in LSB_RELEASE_DATA.split("\n") if line.startswith("DISTRIB_RELEASE=")]
        OS_VERSION = OS_VERSION[0] if OS_VERSION else ""
        OS_FULLNAME = [line.split("=")[1].strip('"') for line in LSB_RELEASE_DATA.split("\n") if line.startswith("DISTRIB_DESCRIPTION=")]
        OS_FULLNAME = OS_FULLNAME[0] if OS_FULLNAME else ""
    else:
        # Catch all, in case it's unclear what specific release this is.
        OS_FULLNAME = f"Debian {OS_VERSION}"
        LINUX_VERSION = "Debian"

# Ubuntu test (optional) `grep "[Uu]buntu" /proc/version`

# E-smith
if os.path.exists("/etc/e-smith-release"):
    with open("/etc/e-smith-release") as file:
        OS_FULLNAME = file.read().strip()

# Gentoo
if os.path.exists("/etc/gentoo-release"):
    with open("/etc/gentoo-release") as file:
        OS_FULLNAME = file.read().strip()
# Red Hat and others
if os.path.exists("/etc/redhat-release"):
    OS_REDHAT_OR_CLONE = 1

    # CentOS
    if "CentOS" in open("/etc/redhat-release").read():
        OS_FULLNAME = "CentOS"
        LINUX_VERSION = "CentOS"
        OS_VERSION = OS_FULLNAME

    # BCLinux
    if "BigCloud" in open("/etc/redhat-release").read():
        OS_FULLNAME = "BigCloud"
        LINUX_VERSION = "BCLinux"
        OS_VERSION = OS_FULLNAME

    # ClearOS
    if "ClearOS" in open("/etc/redhat-release").read():
        OS_FULLNAME = "ClearOS"
        LINUX_VERSION = "ClearOS"
        OS_VERSION = OS_FULLNAME

    # Fedora
    if "Fedora" in open("/etc/redhat-release").read():
        OS_FULLNAME = "Fedora"
        OS_VERSION = OS_FULLNAME
        LINUX_VERSION = "Fedora"

    # Mageia (has also /etc/megaia-release)
    if "Mageia" in open("/etc/redhat-release").read():
        OS_FULLNAME = [line for line in open("/etc/redhat-release").readlines() if line.startswith("Mageia")][0].strip()
        OS_VERSION = [line.split()[2] for line in open("/etc/redhat-release").readlines() if line.startswith("Mageia")][0]
        LINUX_VERSION = "Mageia"

    # Oracle Enterprise Linux
    if "Enterprise Linux Enterprise Linux Server" in open("/etc/redhat-release").read():
        LINUX_VERSION = "Oracle Enterprise Linux"
        OS_FULLNAME = [line for line in open("/etc/redhat-release").readlines() if "Enterprise Linux" in line][0].strip()
        OS_VERSION = OS_FULLNAME

    # Oracle Enterprise Linux
    if "Oracle Linux Server" in open("/etc/oracle-release").read():
        LINUX_VERSION = "Oracle Enterprise Linux"
        OS_FULLNAME = [line for line in open("/etc/oracle-release").readlines() if "Oracle Linux" in line][0].strip()
        OS_VERSION = OS_FULLNAME

    # Oracle VM Server
    if os.path.exists("/etc/ovs-release"):
        if "Oracle VM" in open("/etc/ovs-release").read():
            LINUX_VERSION = "Oracle VM Server"
            OS_FULLNAME = [line for line in open("/etc/ovs-release").readlines() if "Oracle VM" in line][0].strip()
            OS_VERSION = OS_FULLNAME

    # Red Hat
    if "Red Hat" in open("/etc/redhat-release").read():
        OS_FULLNAME = [line for line in open("/etc/redhat-release").readlines() if "Red Hat" in line][0].strip()
        OS_VERSION = OS_FULLNAME
        LINUX_VERSION = "Red Hat"

    # Scientific
    if "Scientific" in open("/etc/redhat-release").read():
        OS_FULLNAME = [line for line in open("/etc/redhat-release").readlines() if line.startswith("Scientific")][0].strip()
        OS_VERSION = [line.split()[3] for line in open("/etc/redhat-release").readlines() if line.startswith("Scientific")][0]
        LINUX_VERSION = "Scientific"

# PCLinuxOS
if pathlib.Path('/etc/pclinuxos-release').is_file():
    with open('/etc/pclinuxos-release', 'r') as file:
        FIND = re.search(r'^PCLinuxOS', file.read(), re.MULTILINE)
        if FIND:
            OS_FULLNAME = "PCLinuxOS Linux"
            LINUX_VERSION = "PCLinuxOS"
            with open('/etc/pclinuxos-release', 'r') as file:
                OS_VERSION = re.search(r'^PCLinuxOS.*release (\w+)', file.read(), re.MULTILINE).group(1)

# Sabayon Linux
if pathlib.Path('/etc/sabayon-edition').is_file():
    with open('/etc/sabayon-edition', 'r') as file:
        FIND = re.search(r'Sabayon Linux', file.read(), re.MULTILINE)
        if FIND:
            OS_FULLNAME = "Sabayon Linux"
            LINUX_VERSION = "Sabayon"
            with open('/etc/sabayon-edition', 'r') as file:
                OS_VERSION = file.read().split()[2]

# SLOX
if pathlib.Path('/etc/SLOX-release').is_file():
    with open('/etc/SLOX-release', 'r') as file:
        FIND = re.search(r'SuSE Linux', file.read(), re.MULTILINE)
        if FIND:
            OS_FULLNAME = FIND.group(0)
            LINUX_VERSION = "SuSE"

# Slackware
if pathlib.Path('/etc/slackware-version').is_file():
    with open('/etc/slackware-version', 'r') as file:
        LINUX_VERSION = "Slackware"
        OS_VERSION = re.search(r'^Slackware (\w+)', file.read(), re.MULTILINE).group(1)
        OS_FULLNAME = f"Slackware Linux {os_version}"

# SuSE
if pathlib.Path('/etc/SuSE-release').exists():
    with open('/etc/SuSE-release', 'r') as file:
        OS_VERSION = file.readline().strip()
        LINUX_VERSION = "SuSE"

# Turbo Linux
if pathlib.Path('/etc/turbolinux-release').exists():
    with open('/etc/turbolinux-release', 'r') as file:
        OS_FULLNAME = file.read().strip()

# YellowDog
if pathlib.Path('/etc/yellowdog-release').exists():
    with open('/etc/yellowdog-release', 'r') as file:
        OS_FULLNAME = file.read().strip()

# VMware
if pathlib.Path('/etc/vmware-release').exists():
    with open('/etc/vmware-release', 'r') as file:
        OS_FULLNAME = file.read().strip()
        OS_VERSION = platform.uname().release
        IS_VMWARE_ESXI = subprocess.getoutput('vmware -vl | grep "VMware ESXi"')
        if IS_VMWARE_ESXI:
            OS_FULLNAME = f"VMware ESXi {os_version}"
if LINUX_VERSION and OS_NAME == "Linux":
    OS_NAME = LINUX_VERSION

# If Linux version (full name) is unknown, use uname value
if not OS_FULLNAME:
    OS_FULLNAME = platform.uname().release

SYSCTL_READKEY = "sysctl -n"
#print("os_name: ", OS_FULLNAME, " os_version: ", OS_VERSION, "os_name: ", OS_NAME)
#print("system: ", SYSTEM, " release: ", RELEASE, "machine: ", MACHINE)
# NetBSD
if SYSTEM == "NetBSD":
    OS_NAME = "NetBSD"
    OS_FULLNAME = f"{platform.uname().system} {platform.uname().release}"
    OS_KERNELVERSION = platform.uname().version
    OS_VERSION = platform.uname().release
    HARDWARE = platform.uname().machine
    FIND_BINARIES = "whereis"
    SYSCTL_READKEY = ""

# OpenBSD
if SYSTEM == "OpenBSD":
    OS_NAME = "OpenBSD"
    OS_FULLNAME = f"{platform.uname().system} {platform.uname().release}"
    OS_KERNELVERSION = platform.uname().version
    OS_VERSION = platform.uname().release
    HARDWARE = platform.uname().machine
    FIND_BINARIES = "whereis"
    SYSCTL_READKEY = ""

# Solaris / OpenSolaris
if SYSTEM == "SunOS":
    OS_NAME = "Sun Solaris"
    OS_FULLNAME = f"{platform.uname().system} {platform.uname().release}"
    OS_VERSION = platform.uname().release
    HARDWARE = platform.uname().machine
    if subprocess.getoutput('/usr/bin/isainfo'):
        OS_MODE = subprocess.getoutput('/usr/bin/isainfo -b')
    SYSCTL_READKEY = ""

# VMware products
if SYSTEM == "VMkernel":
    SYSTEM = "VMware"
    OS_FULLNAME = ""
    OS_VERSION = ""
    HARDWARE = platform.uname().machine
    if pathlib.Path('/etc/vmware-release').exists():
        with open('/etc/vmware-release', 'r') as file:
            OS_FULLNAME = file.read().strip()
            OS_VERSION = platform.uname().release
    HAS_VMWARE_UTIL = subprocess.getoutput('which vmware 2> /dev/null')
    if HAS_VMWARE_UTIL:
        IS_VMWARE_ESXI = subprocess.getoutput('vmware -vl | grep "VMware ESXi"')
        if IS_VMWARE_ESXI:
            OS_NAME = "VMware ESXi"
            OS_FULLNAME = f"VMware ESXi {OS_VERSION}"
# Unknown or unsupported systems
if SYSTEM not in ["AIX", "Darwin", "DragonFly", "FreeBSD", "HP-UX", "NetBSD", "OpenBSD", "SunOS", "Linux", "VMkernel", "MacOS", "Solaris"]:
    print("[ WARNING ]")
    print("Error: Unknown OS found. No support available yet for this OS or platform...")
    print("Please consult the README/documentation for more information.")
    exit(1)

# Set correct echo binary and parameters after detecting operating system
ECHONB = ""

if SYSTEM == "AIX":
    ECHOCMD = "echo"
elif SYSTEM in ["DragonFly", "FreeBSD", "NetBSD"]:
    ECHOCMD = "echo -e"
    ECHONB = "echo -n"
elif SYSTEM == "MacOS":
    ECHOCMD = "echo"
    ECHONB = "echo -n"
elif SYSTEM == "Solaris":
    ECHOCMD = "echo"
elif SYSTEM == "Linux":
    # Check if dash is used (Debian/Ubuntu)
    DEFAULT_SHELL = subprocess.getoutput('ls -l /bin/sh | awk -F\'>\' \'{print $2}\'')
    if DEFAULT_SHELL == " dash":
        ECHOCMD = "/bin/echo -e"
    else:
        ECHOCMD = "echo -e"
else:
    ECHOCMD = "echo -e"

# Check if we have full featured commands, or are using BusyBox as a shell
if pathlib.Path('/bin/busybox').exists():
    if pathlib.Path('/bin/ps').is_symlink():
        SYMLINK_PATH = pathlib.Path('/bin/ps').resolve()
        if SYMLINK_PATH == pathlib.Path('/bin/busybox'):
            SHELL_IS_BUSYBOX = 1
