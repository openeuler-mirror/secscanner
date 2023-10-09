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
import gen_report.report as report
from datetime import datetime
import json
from db.cvrf import *
import urllib.request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
logger = logging.getLogger('secscanner')

def restart_service(service_name):
    subprocess.run(['systemctl', 'restart', service_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_service(service_name):
    subprocess.run(['systemctl', 'start', service_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# show the check result overview
def scan_show_result():
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print(f"  #   "+MAGENTA+"Show the checking result overview..."+WHITE+" "*26+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)
    report_datetime_end = datetime.now()
    set_value("report_datetime_end",report_datetime_end)
    report.main()

# check the system
def scan_check_sys():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print(f"  #   {MAGENTA}Starting check the system basically..."+WHITE+" "*24+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)

    RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

    if os.access(RESULT_FILE, os.W_OK):
        open(RESULT_FILE, "w").close()
    else:
        open(RESULT_FILE, "a").close()
    pattern = r'C([0-9]+)_.*\.py'

    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "bsc_check")
    CHECK_ITEMS = sorted(glob.glob( path + '/*' ))

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
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Starting check the system rootkit..." + WHITE + " "*26 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)

    RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

    if os.access(RESULT_FILE, os.W_OK):
        open(RESULT_FILE, "w").close()
    else:
        open(RESULT_FILE, "a").close()

    pattern = r'R([0-9]+)_.*\.py'
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "intrusion_check")
    CHECK_ITEMS = sorted(glob.glob(path + '/*'))
    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
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

# fix the system
def scan_fix_sys():
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print(f"  #   {MAGENTA}Basicly fix the system..."+WHITE+" "*37+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)

    OS_ID = get_value("OS_ID")
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "bsc_set")
    CHECK_SET = sorted(glob.glob(path + '/*'))
    pattern = r'S([0-9]+)_.*\.py'

    if os.path.isfile(RESULT_FILE) and os.path.getsize(RESULT_FILE) > 0:
        print(f"Begin to fix the system warnings, according to checking-result...")
        with open(RESULT_FILE) as result_file:

            for line in result_file:
                if not line.strip().startswith('#') and not line.strip() == "":
                    ifix = line.split()[0].split('C')[-1]
                    s_pattern = r'S' + ifix + r'_.*\.py'
                    for i in CHECK_SET:
                        match = re.search(s_pattern, i )
                        if match:
                            module_name = os.path.splitext(os.path.basename(i))[0]
                            module_path = os.path.dirname(i)
                            sys.path.append(module_path)
                            try:
                                module = __import__(module_name)
                                getattr(module, module_name)()
                                break
                            except:
                                pass

            open(RESULT_FILE, 'w').close()
            os.remove(RESULT_FILE)
    else:
        print(f"Begin to fix the {OS_ID} system warnings, without checking-result...")
        for iFix in CHECK_SET:
            match = re.search(pattern, iFix)
            if match:
                s_num = int(match.group(1))
                if 1 <= s_num <= 60 and os.path.isfile(iFix):
                    module_name = os.path.splitext(os.path.basename(iFix))[0]
                    module_path = os.path.dirname(iFix)
                    sys.path.append(module_path)
                    #print(f"Fixing items using {iFix}...")
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
    unused_users = seconf.get('basic', 'unused_user_value').split()
    for user in unused_users:
        grep_output = subprocess.run(['grep', user, '/etc/passwd'], capture_output=True, text=True)
        if grep_output.returncode == 0:
            usermod_process = subprocess.run(['usermod', '-U', '-s', '/sbin/nologin', user])
            if usermod_process.returncode == 0:
                Display(f"- Restoring unused {user}...", "FINISHED")

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
        #print(dest_path)
        #print(source_path)
        if os.path.isfile(dest_path):
            logger.info(f'Found bak file: {source_path}, starting restore')
            Display(f"- Restoring cfg file: {source_path}...", "FINISHED")
            if os.path.isfile(source_path):
                shutil.move(source_path, f'{source_path}_user_modifyed')
            shutil.move(dest_path, source_path)
        else:
            logger.warning(f'No {source_path} bak config file was found')
            Display(f"- Restoring cfg file: {source_path}...", "SKIPPED")

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


    property_file = ['/etc/secscanner.d/fdproperty_record', '/etc/secscanner.d/fdproperty_record']

    for i in property_file:
        if os.path.isfile(i):
            with open(i, 'r') as file:
                restore_file = file.read().splitlines()
                for i in restore_file:
                    name = i.split('=')[0]
                    if os.path.exists(name):
                        pro_val = i.split('=')[1]
                        pro_val = int(pro_val, 8)
                        os.chmod(name, pro_val)
                    Display(f"- Restoring property of file or dir:{name}...", "FINISHED")

    restore_unused_user()

    if os.path.isfile(RESULT_FILE):
        open(RESULT_FILE, 'w').close()
    if os.path.isfile(RESULT_FILE):
        os.remove(RESULT_FILE)


def scan_restore_basic_settings():
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print("  #   "+MAGENTA+"Restore Basic settings..."+WHITE+" "*37+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)

    #auto do the restore
    AUTO_BASIC_RESTORE = get_value("AUTO_BASIC_RESTORE")
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

def scan_vulnerabilities_db():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Start updating the system vulnerabilities database..." + WHITE + " " * 18 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    cvrf_index = scrapy_CVRF_index()
    engine = create_engine('sqlite:///secScanner/db/cvedatabase.db', echo=False)
    DBModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    update_count = 0
    for i, url in enumerate(cvrf_index):
        url = url.strip()
        cur = url.strip('.xml').split('cvrf-')[1]
        if session.query(CVRF).filter_by(securityNoticeNo=f'{cur}').first():
            continue

        download_url = os.path.join("https://repo.openeuler.org/security/data/cvrf/", url)
        print("this is download url: ", download_url)
        print("this is url: ", url)
        request = urllib.request.Request(download_url)
        # request = urllib.request.Request("https://repo.openeuler.org/security/data/cvrf/2023/cvrf-openEuler-SA-2023-1554.xml")
        request.add_header("Range", "bytes={}-".format(0))
        text = urllib.request.urlopen(request).read().decode('utf-8')

        cvrf_xml_handler = CVRFXML(text)
        print(cvrf_xml_handler.node_get_securityNoticeNo())

        cvrf = CVRF()
        cvrf.securityNoticeNo = cvrf_xml_handler.node_get_securityNoticeNo()
        cvrf.affectedComponent = cvrf_xml_handler.node_get_affectedComponent()
        cvrf.announcementTime = cvrf_xml_handler.node_get_announcetime()
        cvrf.updateTime = cvrf_xml_handler.node_get_updatetime()
        cvrf.type = cvrf_xml_handler.node_get_type()
        cvrf.cveId = ";".join(cvrf_xml_handler.node_get_cveId()) + ';'
        cvrf.cveThreat = ";".join(cvrf_xml_handler.node_get_cveThreat()) + ';'
        print("cveid", cvrf.cveId)
        print("cvethreat", cvrf.cveThreat)
        cvrf.affectedProduct = ";".join(cvrf_xml_handler.node_get_affectedProduct()) + ';'
        pkg_dict = cvrf_xml_handler.node_get_packageName()
        cvrf.packageName = str(pkg_dict)
        session.add(cvrf)
        session.commit()
        update_count = update_count + 1
    session.close()
    print("Update database done!")
    print(f"{update_count} date updated!")


    scan_show_result()

def scan_vulnerabilities_db_show():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Show some data from cvedatabase..." + WHITE + " " * 18 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    engine = create_engine('sqlite:///secScanner/db/cvedatabase.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(20):
        our_sample = session.query(CVRF).filter_by(id=f'{i + 1}').first()
        if type(our_sample) == CVRF:
            print(our_sample.securityNoticeNo)
            print(our_sample.cveId)
            print(our_sample.cveThreat)
    session.close()

def scan_vulnerabilities_db_create_oval(xml_path = '/db/', table = CVRF):
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Generate an OVAL file from existing cvedatabase..." + WHITE + " " * 18 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    engine = create_engine('sqlite:///secScanner/db/cvedatabase.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    t = time.strftime("%Y-%m-%dT%X", time.localtime())
    dir = os.path.dirname(os.path.abspath(__file__))
    all_samples = session.query(table).order_by(desc('id')).all()
    with open(dir + xml_path+table.__tablename__+'_oval.xml', 'w') as write_file:
        write_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        write_file.write("<oval_definitions \n")
        write_file.write("xsi:schemaLocation=\"http://oval.mitre.org/XMLSchema/oval-definitions-5#linux linux-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-definitions-5#unix unix-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-definitions-5 oval-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-common-5 oval-common-schema.xsd\"\n")
        write_file.write("xmlns=\"http://oval.mitre.org/XMLSchema/oval-definitions-5\"\n")
        write_file.write("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
        write_file.write("xmlns:oval=\"http://oval.mitre.org/XMLSchema/oval-common-5\"\n")
        write_file.write("xmlns:oval-def=\"http://oval.mitre.org/XMLSchema/oval-definitions-5\">\n")
        write_file.write("<generator>\n")
        write_file.write("<oval:product_name>Marcus Updateinfo to OVAL Converter</oval:product_name>\n")
        write_file.write("<oval:schema_version>5.5</oval:schema_version>\n")
        write_file.write(f"<oval:timestamp>{t}</oval:timestamp>\n")
        write_file.write("</generator>\n")
        write_file.write("<definitions>\n")
        for take_a_sample in all_samples:
            field_list = list(take_a_sample.__dict__)
            make_oval_definition(take_a_sample, field_list, write_file)
        write_file.write("</definitions>\n")
        write_file.write("</oval_definitions>\n")
    session.close()

def scan_vulnerabilities_rpm_check():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Check system rpm by db data..." + WHITE + " " * 18 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    engine = create_engine('sqlite:///secScanner/db/cvedatabase.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    euler_version = get_value('SYS_VERSION')
    # all 20.30 openeulers' rpm contains "oe1" suffix, when Euler version >= 22.03, change oe1 to oe2203 instead
    ver_rpm = 'oe1'
    if euler_version == '22.10U1 LTS' or euler_version == '22.03 LTS SP1':
        euler_version = 'openEuler-22.03-LTS-SP1'
        ver_rpm = 'oe2203sp1'
    elif euler_version == '22.10 LTS' or euler_version == '22.03 LTS':
        euler_version = 'openEuler-22.03-LTS'
        ver_rpm = 'oe2203'
    elif euler_version == '22.10U2 LTS' or euler_version == '22.03 LTS SP2':
        euler_version = 'openEuler-22.03-LTS-SP2'
        ver_rpm = 'oe2203sp2'
    elif euler_version == '21.10U3 LTS' or euler_version == '20.03 LTS SP3':
        euler_version = 'openEuler-20.03-LTS-SP3'
    elif euler_version == '21.10 LTS' or euler_version == '20.03 LTS SP2':
        euler_version = 'openEuler-20.03-LTS-SP2'
    elif euler_version == '20.03 LTS SP1':
        euler_version = 'openEuler-20.03-LTS-SP1'
    #check system archtecture
    Shell_run = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE)
    sys_arch = Shell_run.stdout.decode().strip('\n')

    # use "for" loop to traverse the cve database
    scan_db_sample = session.query(CVRF).all()
    # use a dict to save results
    result_dict = {}
    for i in range(len(scan_db_sample)):
        take_a_sample = scan_db_sample[i]
        aff_component = take_a_sample.affectedComponent
        cve_info = take_a_sample.cveId
        sa_info = take_a_sample.securityNoticeNo
        db_package = take_a_sample.packageName
        temp = re.sub('\'', '\"', db_package)
        db_package_json = json.loads(temp)

        if euler_version in db_package_json:
            db_package_euler = db_package_json[euler_version]
            rpm_list = db_package_euler[sys_arch]
        else:
            # print("This SA didnt update rpm for this system, System maybe safe by now!")
            continue

        #Check system software version
        Shell_run = subprocess.run(['rpm', '-qa', aff_component], stdout=subprocess.PIPE)
        Shell_out = Shell_run.stdout.decode()
        if Shell_out == '':
            #print("This machine doesnt have this software, pass!")
            continue
        else:
            sys_package = Shell_out.strip()

        #get system software's version
        ver_arch = sys_package.split(aff_component)[1]
        ver_arch_list = ver_arch.split('-')
            #ver_last_num: number after "-"
        ver_last_num = ver_arch_list[2].split('.')[0]
        sys_rpm_version = ver_arch_list[1].split('.')
        sys_rpm_version.append(ver_last_num)
        sa_rpm_version = []
        #get SA rpm's version
        found_rpm = ''
        for item in rpm_list:
            if item != '' and (aff_component in item):
                sa_rpm = item.split('.rpm')[0].split('.' + sys_arch)[0].split('.' + ver_rpm)[0].split(aff_component + '-')[1]
            else:
                continue
            temp = sa_rpm.split('-')
            if len(temp) == 2:
                sa_ver_last_num = temp[1]
                sa_rpm_version = temp[0].split('.')
                sa_rpm_version.append(sa_ver_last_num)
                #print("----------This is SA rpm version: ", sa_rpm_version)
                found_rpm = item
                break
        if len(sys_rpm_version) == len(sa_rpm_version):
            for j in range(len(sys_rpm_version)):
                if sys_rpm_version[j] < sa_rpm_version[j]:
                    # print("-----------------There is a rpm need to update!")
                    # print("-----------------system rpm: ", sys_rpm_version)
                    # print("---------------------sa rpm: ", sa_rpm_version)
                    if aff_component not in result_dict:
                        result_dict[aff_component] = []
                        result_dict[aff_component].append(sa_info)
                        result_dict[aff_component].append(cve_info)
                        result_dict[aff_component].append(found_rpm)
                    else:
                        result_dict[aff_component].append(sa_info)
                        result_dict[aff_component].append(cve_info)
                        result_dict[aff_component].append(found_rpm)
                    break

    for s in result_dict:
        print("------------------------------------------------------------------------\n")
        print(f"According to {result_dict[s][0]}")
        print(f"Fix {result_dict[s][1]}")
        print(f"{s} need to update!")
        print("rpm are as follows...")
        print(result_dict[s][2])
    session.close()