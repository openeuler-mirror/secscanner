import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
import pathlib
logger = logging.getLogger("secscanner")


def S11_sshAlgorithms():
    InsertSection("Set the ssh algorithms...")
    SET_SSH_ALORITHMS = seconf.get('basic', 'set_ssh_algorithms')
    SSH_KexAlgorithms_VALUE = seconf.get('basic', 'ssh_kexalgorithms_value')
    SSH_CIPHER_VALUE = seconf.get('basic', 'ssh_cipher_value')
    SSH_MACS_VALUE = seconf.get('basic', 'ssh_macs_value')

    if SET_SSH_ALORITHMS == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        if not os.path.exists('/etc/ssh/ssh_config_bak'):
            shutil.copy2('/etc/ssh/ssh_config', '/etc/ssh/ssh_config_bak')

        IS_EXIST = 0
        IS_EXIST1 = 0
        IS_EXIST2 = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line) and re.search('KexAlgorithms', line)):
                    IS_EXIST = 1
                if (not re.match('#|$', line) and re.search('Cipher', line)):
                    IS_EXIST1 = 1
                if (not re.match('#|$', line) and re.search('MACs', line)):
                    IS_EXIST2 = 1
        if IS_EXIST == 0 :
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\n')
                add_file.write(SSH_KexAlgorithms_VALUE)
                add_file.write('\n')
            with open('/etc/ssh/ssh_config', 'a') as add_file:
                add_file.write('\n')
                add_file.write(SSH_KexAlgorithms_VALUE)
                add_file.write('\n')
        if IS_EXIST1 == 0 :
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\n')
                add_file.write(SSH_CIPHER_VALUE)
                add_file.write('\n')
            with open('/etc/ssh/ssh_config', 'a') as add_file:
                add_file.write('\n')
                add_file.write(SSH_CIPHER_VALUE)
                add_file.write('\n')
        if IS_EXIST2 == 0:
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\n')
                add_file.write(SSH_MACS_VALUE)
                add_file.write('\n')
            with open('/etc/ssh/ssh_config', 'a') as add_file:
                add_file.write('\n')
                add_file.write(SSH_MACS_VALUE)
                add_file.write('\n')

        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#|$', line) and re.search('KexAlgorithms', line):
                    IS_EXIST = 1
                if not re.match('#|$', line) and re.search('Cipher', line):
                    IS_EXIST1 = 1
                if not re.match('#|$', line) and re.search('MACs', line):
                    IS_EXIST2 = 1
        if IS_EXIST == 0:
            logger.info("set the ssh KexAlgorithms failed, no KexAlgorithms config options found")
            Display(f"- Set the ssh KexAlgorithms...", "FAILED")
        else:
            logger.info("set the ssh KexAlgorithms successfully, or its already has config options")
            Display(f"- Set the ssh KexAlgorithms...", "FINISHED")
        if IS_EXIST1 == 0:
            logger.info("set the ssh cipher failed, no cipher config options found")
            Display(f"- Set the ssh cipher...", "FAILED")
        else:
            logger.info("set the ssh cipher successfully, or its already has config options")
            Display(f"- Set the ssh cipher...", "FINISHED")
        if IS_EXIST2 == 0:
            logger.info("set the ssh MACs failed, no MACs config options found")
            Display(f"- Set the ssh MACs...", "FAILED")
        else:
            logger.info("set the ssh MACs successfully, or its already has config options")
            Display(f"- Set the ssh MACs...", "FINISHED")
    else:
        Display(f"- Skip set ssh algorithms due to config file...", "SKIPPING")