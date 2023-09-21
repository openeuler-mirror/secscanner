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
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from secScanner.gconfig import *
from secScanner.scan_func import scan_fix_sys, scan_check_sys, scan_restore_basic_settings, scan_check_rootkit, scan_vulnerabilities_db, scan_vulnerabilities_db_show

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
    scan_fix_sys()
    scan_check_sys()

def check_basic(args):
    display_info()
    check_isvirtualmachine()
    scan_check_sys()

def check_rootkit(args):
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
    scan_vulnerabilities_db()

def db_show(args):
    display_info()
    check_isvirtualmachine()
    scan_vulnerabilities_db_show()

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
    fix_item_parser.add_argument('item', nargs='?', help="Custom item option", choices=['sshRootDenie', 'issueRemove', 'noOneSU', 'addUser', 'disableUnUsedaliases', 'syslogProperty'])
    fix_item_parser.set_defaults(func=fix_item)

    check_parser = subparsers.add_parser('check', help="Check command")
    check_subparsers = check_parser.add_subparsers(dest='mode')

    check_basic_parser = check_subparsers.add_parser('basic', help="Check the system basicly")
    check_basic_parser.set_defaults(func=check_basic)

    check_rootkit_parser = check_subparsers.add_parser('rootkit', help="Check the system rootkit")
    check_rootkit_parser.set_defaults(func=check_rootkit)

    restore_parser = subparsers.add_parser('restore', help="Restore command")
    restore_subparsers = restore_parser.add_subparsers(dest='mode')

    restore_basic_parser = restore_subparsers.add_parser('basic', help="Restore all basic settings")
    restore_basic_parser.set_defaults(func=restore_basic)
    restore_basic_parser.add_argument('-y', '--yes', action='store_true', help="Assume 'yes' as the answer to prompts")

    db_parser = subparsers.add_parser('db', help="Database command")
    db_subparsers = db_parser.add_subparsers(dest='mode')
    db_update_parser = db_subparsers.add_parser('update', help="Update the database")
    db_update_parser.set_defaults(func=db_update)
    db_show_parser = db_subparsers.add_parser('show', help="Show the database")
    db_show_parser.set_defaults(func=db_show)

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
