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


import argparse
import sys,os
import glob
import re
import importlib
import getpass
from secScanner.commands.check_outprint import *
from secScanner.services import *
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from secScanner.gconfig import * 
from secScanner.scan_func import *


def quiet_output(args):
    QUIET = 1
    QUIET = set_value("QUIET", QUIET)

def fix_basic(args):
    display_info()
    check_isvirtualmachine()
    scan_fix_sys()

def auto(args):
    display_info()
    check_isvirtualmachine()
    scan_check_sys()
    scan_fix_sys()

def check_basic(args):
    display_info()
    check_isvirtualmachine()
    scan_check_sys()

def check_rootkit(args):
    display_info()
    scan_check_rootkit()

def restore_basic(args):
    display_info()
    check_isvirtualmachine()
    AUTO_BASIC_RESTORE = 1 if args.yes else 0
    AUTO_BASIC_RESTORE = set_value("AUTO_BASIC_RESTORE", AUTO_BASIC_RESTORE)  # auto basic restore
    scan_restore_basic_settings()

def fix_item(args):
    display_info()
    check_isvirtualmachine()
    items = ['sshRootDenie', 'issueRemove', 'noOneSU', 'addUser', 'disableUnUsedaliases', 'syslogProperty']
    if args.item not in items:
        print("Invalid item option, please check...")
    else:
        print(WHITE)
        print("  ###################################################################")
        print("  #                                                                 #")
        print(f"  #   {MAGENTA}Fix the specify items...{WHITE}                                      #")
        print("  #                                                                 #")
        print("  ###################################################################")
        print(NORMAL)

        pattern = rf'S([0-9]+)_{args.item}\.py'
        path = r'./secScanner/bsc_set/'
        if os.path.exists(path):
            files = [filename for filename in os.listdir(path) if re.match(pattern, filename)]
            matched_files = [os.path.join(path, filename) for filename in files]
            confirmation = getpass.getpass(f"you are going to call the {args.item}. (y/n): ")
            if confirmation.lower() == 'y' :
                for file in matched_files:
                    module_name = os.path.splitext(os.path.basename(file))[0]
                    module_path = os.path.dirname(file)
                    sys.path.append(module_path)
                    try:
                        module = __import__(module_name)
                        getattr(module, module_name)()
                    except ImportError as e:
                        print(f"Failed to import module {module_name}: {e}")
                        sys.exit(1)
                    except AttributeError as e:
                        print(f"Module {module_name} does not have the required function: {e}")
                        sys.exit(1)
            #需要增加重启服务，sshd或rsyslog代码

            elif confirmation.lower() == 'n':
                print("Access denied. Specified item format is invalid.")

            else:
                print("Wrong input")
        else:
            print(f"file {args.item} does not exist.")
            sys.exit(1)
            
def db_update(args):
    display_info()
    check_isvirtualmachine()
    vulnerabilities_db_update()

def db_oval(args):
    display_info()
    check_isvirtualmachine()
    scan_vulnerabilities_db_create_oval()

def rpm_check(args):
    display_info()
    check_isvirtualmachine()
    scan_vulnerabilities_rpm_check()

def rpm_scan(args):
    display_info()
    check_isvirtualmachine()
    scan_vulnerabilities_by_items()

def get_report(args):
    display_info()
    check_isvirtualmachine()
    scan_check_all()

def service_on(args):
    service = ['secaide', 'sechkrootkit']
    if args.servicename not in service:
        print("Invalid service name, please check...")
    else:
        dir = '/usr/lib/systemd/system/'
        timer_name = rf'{args.servicename}.timer'
        service_name = rf'{args.servicename}.service'
        path_timer = os.path.join(dir, timer_name)
        path_service = os.path.join(dir, service_name)
        if os.path.exists(path_timer):
            if args.servicename == 'secaide':
                obj_init = service_aide()
                obj_init.aide_init()

            obj_on = sec_service()
            obj_on.reload()
            obj_on.is_enabled(timer_name)
            obj_on.start(timer_name)

        else:
            if os.path.exists(path_service):
                obj_on = sec_service()
                obj_on.reload()
                obj_on.is_enabled(service_name)
                obj_on.start(service_name)

def service_off(args):
    service = ['secaide', 'sechkrootkit']
    if args.servicename not in service:
        print("Invalid service name, please check...")
    else:
        dir = '/usr/lib/systemd/system/'
        timer_name = rf'{args.servicename}.timer'
        service_name = rf'{args.servicename}.service'
        path_timer = os.path.join(dir, timer_name)
        path_service = os.path.join(dir, service_name)
        if os.path.exists(path_timer):
            obj_off = sec_service()
            obj_off.stop(timer_name)
            obj_off.disable(timer_name)
            obj_off.stop(service_name)

        else:
            if os.path.exists(path_service):
                obj_off = sec_service()
                obj_off.stop(service_name)
                obj_off.disable(service_name)

def service_status(args):
    service = ['secaide', 'sechkrootkit']
    if args.servicename not in service:
        print("Invalid service name, please check...")
    else:
        dir = '/usr/lib/systemd/system/'
        service_name = rf'{args.servicename}.service'
        path_service = os.path.join(dir, service_name)
        if os.path.exists(path_service):
            obj_status = sec_service()
            obj_status.status(service_name)


def scan_command():

    parser = argparse.ArgumentParser(description='SecScanner command')

    parser.add_argument('--config', action='store_true',  help='Show settings file path')

    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',default=False, help='Quiet mode')
    parser.add_argument('-V', '--version', action='version', version='SecScanner 0.1.0', help='Show version')

    subparsers = parser.add_subparsers(dest='command')
    
    auto_parser = subparsers.add_parser('auto', help="auto command")
    auto_parser.set_defaults(func=auto)

    fix_parser = subparsers.add_parser('fix', help="Fix command")
    fix_subparsers = fix_parser.add_subparsers(dest='mode')

    fix_basic_parser = fix_subparsers.add_parser('basic', help="Basicly fix the system")
    fix_basic_parser.set_defaults(func=fix_basic)

    # Item fix subcommand
    fix_item_parser = fix_subparsers.add_parser('item', help="Fix a specific item")
    fix_item_parser.add_argument('item', nargs='?', help="Custom item option", choices=['sshRootDenie', 'issueRemove', 'noOneSU', 'addUser', 'syslogProperty', 'ftpBanner', 'restrictFTPdir', 'anonymousFTP'])
    fix_item_parser.set_defaults(func=fix_item)

    check_parser = subparsers.add_parser('check', help="Check command")
    check_subparsers = check_parser.add_subparsers(dest='mode')

    check_basic_parser = check_subparsers.add_parser('basic', help="Check the system basicly")
    check_basic_parser.set_defaults(func=check_basic)

    check_rootkit_parser = check_subparsers.add_parser('rootkit', help="Check the system rootkit")
    check_rootkit_parser.set_defaults(func=check_rootkit)

    check_vulner_parser = check_subparsers.add_parser('cve', help="Check the system vulnerability")
    check_vulner_parser.set_defaults(func=rpm_check)
    
    check_vulner_target_parser = check_subparsers.add_parser('cve_t', help="Check the system vulnerability targeted according to cfg file")
    check_vulner_target_parser.set_defaults(func=rpm_scan)
    
    check_all_parser = check_subparsers.add_parser('all', help="Check the system basicly, rootkit and vulnerability, output html report")
    check_all_parser.set_defaults(func=get_report)

    restore_parser = subparsers.add_parser('restore', help="Restore command")
    restore_subparsers = restore_parser.add_subparsers(dest='mode')

    restore_basic_parser = restore_subparsers.add_parser('basic', help="Restore all basic settings")
    restore_basic_parser.set_defaults(func=restore_basic)
    restore_basic_parser.add_argument('-y', '--yes', action='store_true', help="Assume 'yes' as the answer to prompts")

    db_parser = subparsers.add_parser('db', help="Database command")
    db_subparsers = db_parser.add_subparsers(dest='mode')
    
    db_update_parser = db_subparsers.add_parser('update', help="Update the database")
    db_update_parser.set_defaults(func=db_update)
    
    db_oval_parser = db_subparsers.add_parser('oval', help="Generate xml from the database")
    db_oval_parser.set_defaults(func=db_oval)

    # service commands
    service_parser = subparsers.add_parser('service', help="AIDE service command")
    service_parser.add_argument('servicename',  type=str, help="Service name(secaide, sechkrootkit)")
    service_subparsers = service_parser.add_subparsers(dest='action')

    service_on_parser = service_subparsers.add_parser('on', help="Start service")
    service_on_parser.set_defaults(func=service_on)

    service_off_parser = service_subparsers.add_parser('off', help="Stop service")
    service_off_parser.set_defaults(func=service_off)

    service_status_parser = service_subparsers.add_parser('status', help="Check service status")
    service_status_parser.set_defaults(func=service_status)



    args = parser.parse_args()

    find_profile()

    if hasattr(args, 'func'):
        args.func(args)

    if args.config:
        PROFILE = get_value("PROFILE")
        print("")
        print(f"Default config: {PROFILE}")

    if args.quiet:
        quiet_output(args)
