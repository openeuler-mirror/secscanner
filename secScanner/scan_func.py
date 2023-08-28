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


from secScanner.gconfig import *
from secScanner.lib import *
import os
import subprocess
import logging
import time
import glob
import ast
import shutil
import getpass
import sys

logger = logging.getLogger('secscanner')

def Maid():
    print("")
    print("Interrupt detected.")

    RemovePIDFile()
    RemoveTempFiles()

    cleanup()

    Display("- Cleaning up...", "DONE")

    ExitFatal()

# clean up the tmp file
def cleanup():
    if os.path.isdir(TMP_DIR):
        # print("Clean the TMP file")
        shutil.rmtree(TMP_DIR)

# exit the proc
def die(message):
    print(message)
    cleanup()
    sys.exit(1)

def log(message):
    print("")
    print(f"{PURPLE} {message} {NORMAL}")

def error(message):
    print(f'\033[1;5;31m{message}\033[0;39m')
    sys.exit(1)

def restart_service(service_name):
    subprocess.run(['systemctl', 'restart', service_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_service(service_name):
    subprocess.run(['systemctl', 'start', service_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# show the check result overview
def scan_show_result():
    print(WHITE)
    print("  ###################################################################")
    print("  #                                                                 #")
    print(f"  #   "+MAGENTA+"Show the checking result overview..."+WHITE+"                          #")
    print("  #                                                                 #")
    print("  ###################################################################")
    print(NORMAL)

    time.sleep(TEST_PAUSE_TIME)


# check the system
def scan_check_sys():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print("  ###################################################################")
    print("  #                                                                 #")
    print(f"  #   {MAGENTA}Starting check the system basically...{WHITE}                        #")
    print("  #                                                                 #")
    print("  ###################################################################")
    print(NORMAL) 

    # sleep for TEST_PAUSE_TIME
    # Change TEST_PAUSE_TIME to the desired sleep time
    time.sleep(TEST_PAUSE_TIME)

    
    RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

    if os.access(RESULT_FILE, os.W_OK):
        open(RESULT_FILE, "w").close()
    else:
        open(RESULT_FILE, "a").close()

    pattern = r'C([0-9]+)_.*\.py'
    CHECK_ITEMS = sorted(glob.glob(r'./secScanner/bsc_check/*'))
    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            if 1 <= s_num <= 60 : # 范围验证
                module_name = os.path.splitext(os.path.basename(i))[0]
                module_path = os.path.dirname(i)
                sys.path.append(module_path)
                logger.info("checking the %s", module_name)
                try:
                    module = __import__(module_name)
                    getattr(module, module_name)()

                except ImportError as e:
                    print(f"Failed to import module {module_name}: {e}")
                    sys.exit(1)
                except AttributeError as e:
                    print(f"Module {module_name} does not have the required function: {e}")
                    sys.exit(1)
                logger.info("===---------------------------------------------------------------===\n")

    scan_show_result()

# check the system rootkit
def scan_check_rootkit():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.

    print(WHITE)
    print("  ###################################################################")
    print("  #                                                                 #")
    print(f"  #   {MAGENTA}Starting check the system rootkit...{WHITE}                  #")
    print("  #                                                                 #")
    print("  ###################################################################")
    print(NORMAL)

    # sleep for TEST_PAUSE_TIME
    # Change TEST_PAUSE_TIME to the desired sleep time
    time.sleep(TEST_PAUSE_TIME)

    RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

    if os.access(RESULT_FILE, os.W_OK):
        open(RESULT_FILE, "w").close()
    else:
        open(RESULT_FILE, "a").close()

    pattern = r'R([0-9]+)_.*\.py'
    CHECK_ITEMS = sorted(glob.glob(r'./secScanner/intrusion_check/*'))
    for i in CHECK_ITEMS:
        match = re.match(pattern, i)
        if match:
            s_num = int(match.group(1))
            if 1 == s_num :  # 范围验证
                module_name = os.path.splitext(os.path.basename(i))[0]
                module_path = os.path.dirname(i)
                sys.path.append(module_path)
                logger.info("checking the %s", module_name)
                try:
                    module = __import__(module_name)
                    getattr(module, module_name)()
                except ImportError as e:
                    print(f"Failed to import module {module_name}: {e}")
                    sys.exit(1)
                except AttributeError as e:
                    print(f"Module {module_name} does not have the required function: {e}")
                    sys.exit(1)

                logger.info("===---------------------------------------------------------------===\n")

    scan_show_result()

def fix_items(iFix):
    try:
        subprocess.run(["python3", iFix], check=True)
        time.sleep(TEST_PAUSE_TIME)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {iFix}: {e}")
        sys.exit(1)

# fix the system
def scan_fix_sys():
    print(WHITE)
    print("  ###################################################################")
    print("  #                                                                 #")
    print(f"  #   {MAGENTA}Basicly fix the system...{WHITE}                                     #")
    print("  #                                                                 #")
    print("  ###################################################################")
    print(NORMAL)

    time.sleep(TEST_PAUSE_TIME)
    if os.path.isfile(RESULT_FILE) and os.path.getsize(RESULT_FILE) > 0:
        CHECK_SET = sorted(glob.glob(r'./secScanner/bsc_set/*'))
        pattern = r'S([0-9]+)_.*\.py'
        print(f"Begin to fix the {OS_ID} system warnings, according to checking-result...")
        for line in open(RESULT_FILE):
            if not line.strip().startswith('#') and not line.strip() == "":
                iFix = line.split()[0].split('C')[-1]
                match = re.search(pattern, iFix)
                if match:
                    SET_ITEM = [f for f in CHECK_SET if match.group(0) in f]
                    s_num = int(match.group(1))
                    if len(SET_ITEM) > 0 and 1 <= s_num <= 60 and os.path.isfile(SET_ITEM[0]):
                        module_name = os.path.splitext(os.path.basename(iFix))[0]
                        module_path = os.path.dirname(iFix)
                        sys.path.append(module_path)
                        print(f"Fixing items {iFix} using {SET_ITEM[0]}...")
                        try:
                            module = __import__(module_name)
                            getattr(module, module_name)()
                        except ImportError as e:
                            print(f"Failed to import module {module_name}: {e}")
                            sys.exit(1)
                        except AttributeError as e:
                            print(f"Module {module_name} does not have the required function: {e}")
                            sys.exit(1)

                    else:
                        logger.info(f"Can't fix items {iFix} in this status, try {SET_ITEM[0]} to fix.")
        open(RESULT_FILE, 'w').close()
        os.remove(RESULT_FILE)
    else:
        pattern = r'S([0-9]+)_.*\.py'
        CHECK_SET = sorted(glob.glob(r'./secScanner/bsc_set/*'))
        print(f"Begin to fix the {OS_ID} system warnings, without checking-result...")
        for iFix in CHECK_SET:
            match = re.search(pattern, iFix)
            if match:
                s_num = int(match.group(1))
                if 1 <= s_num <= 60 and os.path.isfile(iFix):
                    module_name = os.path.splitext(os.path.basename(iFix))[0]
                    module_path = os.path.dirname(iFix)
                    sys.path.append(module_path)
                    print(f"Fixing items using {iFix}...")
                    try:
                        module = __import__(module_name)
                        getattr(module, module_name)()
                    except ImportError as e:
                        print(f"Failed to import module {module_name}: {e}")
                        sys.exit(1)
                    except AttributeError as e:
                        print(f"Module {module_name} does not have the required function: {e}")
                        sys.exit(1)
            
    # restart service

    if subprocess.call(['systemctl', 'is-active', 'sshd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        restart_service('sshd')
        print("")
        print(f"{GREEN} Finish restart sshd.service{NORMAL}")
        print("")

    else:
        start_service('sshd')
        print("")
        print(f"{GREEN} Finish start sshd.service{NORMAL}")
        print("")

    if subprocess.call(['systemctl', 'is-active', 'rsyslog'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        restart_service('rsyslog')
        print("")
        print(f"{GREEN} Finish restart rsyslog.service{NORMAL}")
        print("")

    else:
        start_service('rsyslog')
        print("")
        print(f"{GREEN} Finish start rsyslog.service{NORMAL}")
        print("")


    print("")
    print(f"{GREEN} Fix system finished... Now you can recheck the system{NORMAL}")
    print("")


# restore unused  user
def restore_unused_user():
    unused_users = UNUSED_USER_VALUE.split()
    for user in unused_users:
        grep_output = subprocess.run(['grep', user, '/etc/passwd'], capture_output=True, text=True)
        is_exist = len(grep_output.stdout.split('\n')) - 1
        if is_exist != 0:
            subprocess.run(['usermod', '-U', '-s', '/sbin/nologin', user])
            Display("- Restoring unused user...", "FINISHED")

# restore the basic settings
def scan_restore_basic_inline():
    BAK_FILES = ['/etc/motd_bak', '/etc/pam.d/system-auth_bak', '/etc/pam.d/sshd_bak', '/etc/pam.d/password-auth_bak',
                 '/etc/sysctl.conf_bak', '/etc/profile_bak', '/etc/bashrc_bak', '/etc/csh.cshrc_bak',
                 '/etc/csh.login_bak', '/root/.bashrc_bak', '/root/.cshrc_bak', '/etc/login.defs_bak',
                 '/etc/ssh/sshd_config_bak', '/etc/sshbanner_bak', '/etc/ssh/ssh_config_bak', '/etc/securetty_bak',
                 '/etc/syslog.conf_bak', '/etc/rsyslog.conf_bak', '/etc/issue_bak', '/etc/issue.net_bak',
                 '/etc/security/limits.conf_bak', '/etc/vsftpd/vsftpd.conf_bak', '/etc/pam.d/su_bak',
                 '/etc/passwd_bak', '/etc/shadow_bak', '/etc/group_bak', '/etc/aliases_bak', '/etc/mail/aliases_bak']
    for i in BAK_FILES:
        dest_path = i
        source_path = dest_path.strip("_bak")
        print(dest_path)
        print(source_path)
        if os.path.isfile(dest_path):
            logger.info(f'Found bak file: {source_path}, starting restore')
            Display(f"- Restoring cfg file: {source_path}...", "FINISHED")
            if os.path.isfile(source_path):
                shutil.move(source_path, f'{source_path}_user_modifyed')
            shutil.move(dest_path, source_path)
        else:
            logger.warning(f'No {source_path} bak config file was found')
            Display(f"- Restoring cfg file:$i...", "SKIPPED")

    # restart service

    if subprocess.call(['systemctl', 'is-active', 'sshd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        restart_service('sshd')
        logger.info("Restart the service:sshd")
        Display("- Restart service:sshd...", "FINISHED")
    else:
        start_service('sshd')
        logger.info("Restart the service:sshd")
        Display("- Restart service:sshd...", "FINISHED")

    if subprocess.call(['systemctl', 'is-active', 'rsyslog'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        restart_service('rsyslog')
        logger.info("Restart the service:rsyslog")
        Display("- Restart service:rsyslog...", "FINISHED")
    else:
        start_service('rsyslog')
        logger.info("Restart the service:rsyslog")
        Display("- Restart service:rsyslog...", "FINISHED")

    restore_unused_user()

    if os.path.isfile(RESULT_FILE):
        open(RESULT_FILE, 'w').close()
    if os.path.isfile(RESULT_FILE):
        os.remove(RESULT_FILE)

def scan_restore_basic_settings():
    print(WHITE)
    print("  ###################################################################")
    print("  #                                                                 #")
    print("  #   "+MAGENTA+"Restore Basic settings..."+WHITE+"                                     #")
    print("  #                                                                 #")
    print("  ###################################################################")
    print(NORMAL)

    #auto do the restore
    if AUTO_BASIC_RESTORE == 1:
        scan_restore_basic_inline()
    else:
        print(YELLOW_BLINK + "Notice" + NORMAL + ":")
        try:
            bb = getpass.getpass("  You know the effect and ready to do it. " + GREEN + "[y/n]" + NORMAL + ": ")
            if bb.strip().lower() == "y" or bb.strip().lower() == "yes":
                scan_restore_basic_inline()
        except KeyboardInterrupt:
            print("")
            print("  Leaving... Remain everything unchanged.")
            sys.exit()

    print("")
    print(GREEN +" Restore basicly finished... Now you can refix the system" + NORMAL)
    print("")


