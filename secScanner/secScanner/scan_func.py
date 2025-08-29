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
from db.cve import *
import urllib.request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
logger = logging.getLogger('secscanner')
#RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

def restart_service(service_name):
    cmd = 'systemctl restart ' + service_name
    ret, result = subprocess.getstatusoutput(cmd)
    if ret != 0:
        logger.error(f"systemd service restart failed —— {result}")
        print(result)
        sys.exit(1)
    else:
        print(f"\n{GREEN} Finish restart {service_name}{NORMAL}")

def start_service(service_name):
    cmd = 'systemctl start ' + service_name
    ret, result = subprocess.getstatusoutput(cmd)
    if ret != 0:
        logger.error(f"systemd service start failed —— {result}")
        print(result)
        sys.exit(1)
    else:
        print(f"\n{GREEN} Finish start {service_name}{NORMAL}")

# show the check result overview
def scan_show_result():
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print(f"  #  {MAGENTA}For details, please check /var/log/secScanner/secscanner.log "+WHITE+" "*2+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)

    report_datetime_end = datetime.now()
    set_value("report_datetime_end",report_datetime_end)
    report.main()

def scan_check_all():
    baseline = seconf.get('main','baseline')
    scan_check_sys(baseline)
    scan_check_rootkit()
    scan_vulnerabilities_rpm_check()
    scan_show_result()

# check the system
def scan_check_sys(baseline):
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print(f"  #   {MAGENTA}Starting check the system basically..."+WHITE+" "*24+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)

    if os.access(RESULT_FILE, os.W_OK):
        open(RESULT_FILE, "w").close()
    else:
        open(RESULT_FILE, "a").close()
    pattern = r'C([0-9]+)_.*\.py'

    dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(dir, "enhance")
    baseline_path = os.path.join(main_path, baseline)
    path = os.path.join(baseline_path, 'check')

    CHECK_ITEMS = sorted(glob.glob( path + '/*' ))
    numbers = []

    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            numbers.append(s_num)

    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            if min(numbers) <= s_num <= max(numbers) and os.path.isfile(i) : # 范围验证
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
    report.warning_results()
   
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
    numbers = []

    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            numbers.append(s_num)

    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            if min(numbers) <= s_num <= max(numbers) and os.path.isfile(i) :  # 范围验证
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

# fix the system
def scan_fix_sys(baseline):
    print(WHITE)
    print(" "*2+"#"*67)
    print(" "*2+"#"+" "*65+"#")
    print(f"  #   {MAGENTA}Basically fix the system..."+WHITE+" "*37+"#")
    print(" "*2+"#"+" "*65+"#")
    print(" "*2+"#"*67)
    print(NORMAL)

    OS_ID = get_value("OS_ID")
    dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(dir, "enhance")
    baseline_path = os.path.join(main_path, baseline)
    path = os.path.join(baseline_path, "set")
    CHECK_SET = sorted(glob.glob(path + '/*'))
    pattern = r'S([0-9]+)_.*\.py'
    numbers = []
    # record ifix in case of repeat
    fix_indices = set()
    if os.path.isfile(RESULT_FILE) and os.path.getsize(RESULT_FILE) > 0:
        print(f"Begin to fix the system warnings, according to checking-result...")
        with open(RESULT_FILE) as result_file:

            for line in result_file:
                if not line.strip().startswith('#') and not line.strip() == "":
                    ifix = line.split()[0].split('C')[-1]
                    s_pattern = r'S' + ifix + r'_.*\.py'
                    for index, i in enumerate(CHECK_SET):
                        match = re.search(s_pattern, i )
                        if match and index not in fix_indices:
                            fix_indices.add(index)
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
                numbers.append(s_num)

        for iFix in CHECK_SET:
            match = re.search(pattern, iFix)
            if match:
                s_num = int(match.group(1))
                if min(numbers) <= s_num and os.path.isfile(iFix):
                    if iFix == CHECK_SET[-1]:
                        break
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
    # save bak files' name from global dict into bak.py file
    write_bak_file()            
    # restart service
    cmd_sshd = 'systemctl is-active sshd'
    ret, result = subprocess.getstatusoutput(cmd_sshd)
    if ret == 0:
        restart_service('sshd')
    else:
        start_service('sshd')

    cmd_rsyslog = 'systemctl is-active rsyslog'
    reflag, output = subprocess.getstatusoutput(cmd_rsyslog)
    if reflag == 0:
        restart_service('rsyslog')
    else:
        start_service('rsyslog')

    print(f"\n{GREEN} Fix system finished... Now you can recheck the system{NORMAL}")


# restore unused  user
def restore_unused_user():
    unused_users = seconf.get('basic', 'unused_user_value').split()
    for user in unused_users:
        ret, result = subprocess.getstatusoutput(f'grep {user} /etc/passwd')
        if ret != 0:
            logger.warning('Command execution failed')
        else:
            ret, out = subprocess.getstatusoutput(f'usermod -U -s /sbin/nologin {user}')
            if ret == 0:
                Display(f"- Restoring unused {user}...", "FINISHED")

# restore the basic settings
def scan_restore_basic_inline():
    # init bak files name list
    BAK_FILES = []
    # read history bak names, save in list
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(f'{dir}/lib/bak.py', "r") as read_file:
        lines = read_file.readlines()
        for line in lines:
            if 'bak' in line and line.strip('\n') not in BAK_FILES:
                BAK_FILES.append(line.strip('\n'))
            else:
                continue
    # clear bak.py file
    with open(f'{dir}/lib/bak.py', "w") as write_file:
        write_file.write('')
    
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

    property_file = ['/etc/secscanner.d/logfile_property', '/etc/secscanner.d/fdproperty_record']

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
            os.remove(i)

    restore_unused_user()

    # restart service
    cmd_sshd = 'systemctl is-active sshd'
    ret, result = subprocess.getstatusoutput(cmd_sshd)
    if ret == 0:
        restart_service('sshd')
    else:
        start_service('sshd')

    cmd_rsyslog = 'systemctl is-active rsyslog'
    reflag, output = subprocess.getstatusoutput(cmd_rsyslog)
    if reflag == 0:
        restart_service('rsyslog')
    else:
        start_service('rsyslog')

    cmd_vsftpd = 'systemctl is-active vsftpd'
    ret, result = subprocess.getstatusoutput(cmd_vsftpd)
    if ret != 0:
        logger.info('vsftpd service already inactive')
    else:
        flag, out = subprocess.getstatusoutput('systemctl stop vsftpd')
        if flag != 0:
            logger.warning('Stop vsftpd service failed')

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

    print("\n" + GREEN +" Restore basically finished... Now you can refix the system" + NORMAL + "\n")


def vulnerabilities_db_update():
    # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    print(WHITE)
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Start updating the system vulnerabilities database..." + WHITE + " " * 9 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    InsertSection("Updating database")
    cvrf_index = scrapy_CVRF_index()
    dir = os.path.dirname(os.path.abspath(__file__))
    engine = create_engine(f'sqlite:///{dir}/db/cvedatabase.db', echo=False)
    DBModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    update_sa = 0
    update_cve = 0
    for i, url in enumerate(cvrf_index):
        url = url.strip()
        cur = url.strip('.xml').split('cvrf-')[1]
        if session.query(CVRF).filter_by(securityNoticeNo=f'{cur}').first():
            continue

        download_url = os.path.join("https://repo.openeuler.org/security/data/cvrf/", url)
        #print("this is download url: ", download_url)
        #print("this is url: ", url)
        request = urllib.request.Request(download_url)
        # request = urllib.request.Request("https://repo.openeuler.org/security/data/cvrf/2023/cvrf-openEuler-SA-2023-1554.xml")
        request.add_header("Range", "bytes={}-".format(0))
        text = urllib.request.urlopen(request).read().decode('utf-8')

        cvrf_xml_handler = CVRFXML(text)
        #print(cvrf_xml_handler.node_get_securityNoticeNo())

        cvrf = CVRF()
        cvrf.title = cvrf_xml_handler.node_get_title()
        cvrf.securityNoticeNo = cvrf_xml_handler.node_get_securityNoticeNo()
        cvrf.affectedComponent = cvrf_xml_handler.node_get_affectedComponent()
        cvrf.announcementTime = cvrf_xml_handler.node_get_announcetime()
        cvrf.synopsis = cvrf_xml_handler.node_get_synopsis()
        cvrf.summary = cvrf_xml_handler.node_get_summary()
        cvrf.topic = cvrf_xml_handler.node_get_topic()
        cvrf.description = cvrf_xml_handler.node_get_description()
        cvrf.updateTime = cvrf_xml_handler.node_get_updatetime()
        cvrf.announcementLevel = cvrf_xml_handler.node_get_announceLevel()
        cvrf.cveId = ";".join(cvrf_xml_handler.node_get_cveId()) + ';'
        # print("cveid", cvrf.cveId)
        cvrf.cveList = str(cvrf_xml_handler.node_get_cve_reference_list())
        pkg_dict = cvrf_xml_handler.node_get_packageName()
        cvrf.packageInfo = str(pkg_dict)
        session.add(cvrf)
        session.commit()
        update_sa += 1

    ####################################################################################
    # get data from api url
    ####################################################################################
    api_url = 'https://www.openeuler.org/api-euler/api-cve/cve-security-notice-server/cvedatabase/findAll'
    page_size = 100  # 单页请求的数量
    cveDatabaseList = []  # 用于存储所有查询结果

    # 初始化参数
    params = {
        "keyword": "",
        "pages": {
            "page": 1,  # 起始页
            "size": page_size
        }
    }
    for i in range(1, 150):
        response = requests.post(url=api_url, json=params, timeout=(10, 30))
        # 检查响应状态
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            return
        # 获取并解析当前页的数据
        current_page_data = json.loads(response.text)
        # 如果当前页无数据，说明已获取完所有数据，退出循环
        if current_page_data["result"]["cveDatabaseList"] == []:
            break

        # 将当前页数据添加到总结果中
        cveDatabaseList.append(current_page_data)

        # 更新下一页参数
        params["pages"]["page"] += 1  # 前往下一页
    cve_list = []
    for cvedata in cveDatabaseList:
        for single in cvedata['result']["cveDatabaseList"]:
            cve_list.append([single['cveId'], single['packageName']])
    ###################################################################################
    # create sqlite database and save data
    ###################################################################################

    count = 0
    for cve_init in reversed(cve_list):
        count = 1 + count
        # only add new data
        if session.query(CVE).filter_by(cveId=f'{cve_init[0]}', packageName=f'{cve_init[1]}').first():
            continue
        cve_url = f'https://www.openeuler.org/api-euler/api-cve/cve-security-notice-server/cvedatabase/getByCveIdAndPackageName?cveId={cve_init[0]}&packageName={cve_init[1]}'
        response = requests.get(url=cve_url, timeout=2)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}, 请重试！")
            # return
            continue

        if 'Required String parameter' in response.text:
            continue
        json_data = json.loads(response.text)['result']

        cve = CVE()
        cve.cveId = json_data['cveId']
        cve.summary = json_data['summary']
        cve.level = json_data['type']

        cve.cvsssCoreNVD = json_data['cvsssCoreNVD']
        cve.cvsssCoreOE = json_data['cvsssCoreOE']

        cve.attackVectorNVD = json_data['attackVectorNVD']
        cve.attackVectorOE = json_data['attackVectorOE']

        cve.attackComplexityNVD = json_data['attackComplexityNVD']
        cve.attackComplexityOE = json_data['attackComplexityOE']

        cve.privilegesRequiredNVD = json_data['privilegesRequiredNVD']
        cve.privilegesRequiredOE = json_data['privilegesRequiredOE']

        cve.userInteractionNVD = json_data['userInteractionNVD']
        cve.userInteractionOE = json_data['userInteractionOE']

        cve.scopeNVD = json_data['scopeNVD']
        cve.scopeOE = json_data['scopeOE']

        cve.confidentialityNVD = json_data['confidentialityNVD']
        cve.confidentialityOE = json_data['confidentialityOE']

        cve.integrityNVD = json_data['integrityNVD']
        cve.integrityOE = json_data['integrityOE']

        cve.availabilityNVD = json_data['availabilityNVD']
        cve.availabilityOE = json_data['availabilityOE']

        cve.status = json_data['status']

        cve.announcementTime = json_data['announcementTime']
        cve.createTime = json_data['createTime']
        cve.updateTime = json_data['updateTime']

        cve.packageName = json_data['packageName']

        extra_url = f'https://www.openeuler.org/api-euler/api-cve/cve-security-notice-server/cvedatabase/getCVEProductPackageList?cveId={cve_init[0]}&packageName={cve_init[1]}'
        response_extra = requests.get(url=extra_url, timeout=(10, 30))
        if 'Required String parameter' in response_extra.text:
            pass
        else:
            extra_data = json.loads(response_extra.text)['result']
            cve.extra_data = str(extra_data)

        session.add(cve)
        session.commit()
        update_cve += 1

    session.close()
    Display(f"{update_sa} SAs and {update_cve} CVEs are updated!", "OK")


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
    dir = os.path.dirname(os.path.abspath(__file__))
    engine = create_engine(f'sqlite:///{dir}/db/cvedatabase.db', echo=False)
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
    print(f"  #   {MAGENTA}Scan system components by db data..." + WHITE + " " * 26 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    InsertSection("Vulnerability scanning...")
    dir = os.path.dirname(os.path.abspath(__file__))
    engine = create_engine(f'sqlite:///{dir}/db/cvedatabase.db', echo=False)
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
    elif euler_version in ['v24 LTS', '22.03 (LTS-SP3)', '24.e1011']:
        euler_version = 'openEuler-22.03-LTS-SP3'
        ver_rpm = 'oe2203sp3'
    elif euler_version == '22.03 (LTS-SP4)':
        euler_version = 'openEuler-22.03-LTS-SP4'
        ver_rpm = 'oe2203sp4'
    elif euler_version == '21.10U3 LTS' or euler_version == '20.03 LTS SP3':
        euler_version = 'openEuler-20.03-LTS-SP3'
    elif euler_version == '21.10 LTS' or euler_version == '20.03 LTS SP2':
        euler_version = 'openEuler-20.03-LTS-SP2'
    elif euler_version == '20.03 LTS SP1':
        euler_version = 'openEuler-20.03-LTS-SP1'

    #check system architecture
    ret, sys_arch = subprocess.getstatusoutput('uname -m')
    if sys_arch not in ['arm', 'x86_64']:
        print("This architecture is not supported by the vulnerability scanning feature at this time")
        sys.exit(1)
    # use "for" loop to traverse the cve database
    scan_db_sample = session.query(CVRF).all()
    # use a dict to save results
    result_dict = {}
    sa_dict = {}
    for i in range(len(scan_db_sample)):
        take_a_sample = scan_db_sample[i]
        aff_component = take_a_sample.affectedComponent
        # ignore openEuler kernel's vulnerabilities
        if 'kernel' in aff_component:
            continue
        cve_info = take_a_sample.cveId
        sa_info = take_a_sample.securityNoticeNo
        db_package = take_a_sample.packageInfo
        temp = re.sub('\'', '\"', db_package)
        db_package_json = json.loads(temp)

        if euler_version in db_package_json:
            db_package_euler = db_package_json[euler_version]
            rpm_list = db_package_euler[sys_arch]
        else:
            # print("This SA didn't update rpm for this system, System maybe safe by now!")
            continue

        #Check system software version
        ret, sys_qa = subprocess.getstatusoutput(f'rpm -qa {aff_component}')
        if sys_qa == '':
            #print("This machine doesnt have this software, pass!")
            continue
        else:
            sys_package = sys_qa

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
            sa_component = aff_component + '-'
            if item != '' and re.match(sa_component, item):
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
                if sys_rpm_version[j].isdigit() and sa_rpm_version[j].isdigit():
                    if int(sys_rpm_version[j]) < int(sa_rpm_version[j]):
                        result_dict[sa_info] = [sa_info, cve_info, found_rpm, aff_component, sys_package]
                        break
                    elif int(sys_rpm_version[j]) > int(sa_rpm_version[j]):
                        break
                else:
                    if sys_rpm_version[j] < sa_rpm_version[j]:
                        result_dict[sa_info] = [sa_info, cve_info, found_rpm, aff_component, sys_package]
                        break
                    elif sys_rpm_version[j] > sa_rpm_version[j]:
                        break
    
    Display(f"Found {len(result_dict)} pieces of information about component vulnerabilities", "WARNING")
    for s in result_dict:
        print("------------------------------------------------------------------------\n")
        # sa_dict[result_dict[s][0]] = result_dict[s][1].strip(';').split(';')
        sa_dict[result_dict[s][0]] = [result_dict[s][1].strip(';').split(';'), result_dict[s][3], result_dict[s][4]]
        print(f"According to {result_dict[s][0]}")
        print(f"Fix {result_dict[s][1].strip(';')}")
        #print(f"{result_dict[s][3]} need to update!")
        #print(f"Latest version rpm: {result_dict[s][2]}")
        print(f"{result_dict[s][3]} should be updated to {result_dict[s][2].split('.oe')[0]}")
        logger.warning(f"According to {result_dict[s][0]}, vulnerabilities of {result_dict[s][3]} are as follows {result_dict[s][1].strip(';')}, latest rpm {result_dict[s][2]} is provided")
    set_value('vulner_info', sa_dict)
    session.close()
    report.cve_result()

def cut_component_version(component, package):
    # get component's version   glibc-2.28-101.el8.src.rpm
    if component == 'kernel':
        # kernel-5.10.0-200.0.0.154.144.bclinux.21.10U4.x86_64
        ver_arch = package.split(component)[1]  # -2.28-101.el8
        ver_arch_list = ver_arch.split('-')  #
        # ver_last_num: number after "-"
        ver_last_five_num = ver_arch_list[2].split('.')  # ['101']
        component_version = ver_arch_list[1].split('.')  # ['2', '28']
        for i in range(5):
            component_version.append(ver_last_five_num[i])  # ['2', '28', '101']
        return component_version
    ver_arch = package.split(component)[1]  # -2.28-101.el8
    ver_arch_list = ver_arch.split('-')  #
    # ver_last_num: number after "-"
    ver_last_num = ver_arch_list[2].split('.')[0]  # ['101']
    component_version = ver_arch_list[1].split('.')  # ['2', '28']
    component_version.append(ver_last_num)  # ['2', '28', '101']
    return component_version

def compare_version_of_two(sys, sa):
    for i in range(len(sys)):
        if sys[i] == sa[i]:
            continue
        if sys[i].isdigit() and sa[i].isdigit():
            if int(sys[i]) < int(sa[i]):
                return 1
            else:
                continue
        else:
            if sys[i] < sa[i]:
                return 1
    return 0

def scan_vulnerabilities_by_items():
    print(WHITE)
    print(" " * 2 + "#" * 67)
    print(" " * 2 + "#" + " " * 65 + "#")
    print(f"  #   {MAGENTA}Check system components targeted according to cfg file..." + WHITE + " " * 4 + "#")
    print(" " * 2 + "#" + " " * 65 + "#")
    print(" " * 2 + "#" * 67)
    print(NORMAL)
    dir = os.path.dirname(os.path.abspath(__file__))
    engine = create_engine(f'sqlite:///{dir}/db/cvedatabase.db', echo=False)
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
    elif euler_version in ['v24 LTS', '22.03 (LTS-SP3)', '24.e1011']:
        euler_version = 'openEuler-22.03-LTS-SP3'
        ver_rpm = 'oe2203sp3'
    elif euler_version == '21.10U3 LTS' or euler_version == '20.03 LTS SP3':
        euler_version = 'openEuler-20.03-LTS-SP3'
    elif euler_version == '21.10 LTS' or euler_version == '20.03 LTS SP2':
        euler_version = 'openEuler-20.03-LTS-SP2'
    elif euler_version == '20.03 LTS SP1':
        euler_version = 'openEuler-20.03-LTS-SP1'
    #check system architecture
    ret, sys_arch = subprocess.getstatusoutput('uname -m')
    if sys_arch not in ['arm', 'x86_64']:
        print("This architecture is not supported by the vulnerability scanning feature at this time")
        sys.exit(1)

    # Check system software version
    RPM_ASSEMBLY = seconf.get('basic', 'rpm_assembly').split()
    InsertSection("Vulnerability targeted scanning...")
    result_dict = {}
    sa_dict = {}
    for component in RPM_ASSEMBLY:
        ret, sys_qa = subprocess.getstatusoutput(f'rpm -qa {component}')
        if sys_qa == '':
            Display(f"This machine doesn't have [{component}], pass...", "SKIPPING")
            continue
        else:
            sys_package = sys_qa
        # get system software's version   glibc-2.28-101.el8.src.rpm
        sys_rpm_version = cut_component_version(component, sys_package)

        target_sa = session.query(CVRF).order_by(CVRF.id.desc()).all()
        sa_rpm = ''
        sa_num = ''
        cve_list = []
        for single_sa in target_sa:
            if single_sa.affectedComponent != component:
                continue
            else:
                # get SA rpm's version
                packages = re.sub('\'', '\"', single_sa.packageInfo)
                packages_dict = json.loads(packages)
                if euler_version in packages_dict:
                    sa_rpm_list = packages_dict[euler_version][sys_arch]
                else:
                    continue
                #glibc-2.28-101.el8.src.rpm
                for item in sa_rpm_list:
                    if item != '' and (component in item):
                        temp = item.split(component + '-')[1]
                        if temp[0].isdigit():
                            sa_rpm = item
                            sa_num = single_sa.securityNoticeNo
                            #cve_list = single_sa.cveId
                            for i in single_sa.cveId.split(';'):
                                if i != '':
                                    cve_list.append(i)
                            # found target rpm
                            break
                    else:
                        continue
                if sa_rpm != '':
                    break
                else:
                    continue
        if sa_rpm == '':
            Display(f"Can't find any SA data about [{component}] in database...", "SKIPPING")
            continue
        sa_component_version = cut_component_version(component, sa_rpm)
        if len(sa_component_version) == len(sys_rpm_version):
            if compare_version_of_two(sys_rpm_version, sa_component_version):
                result_dict[component] = [sys_package, sa_rpm, 1]
                logger.warning(f"According to {sa_num}, vulnerabilities of {component} are as follows {cve_list}, latest rpm {sa_rpm} is provided")
                Display(f"[{component}] should be updated to {sa_rpm.split('.oe')[0]}...", "WARNING")
                sa_dict[sa_num] = [cve_list, component, sa_rpm]
            else:
                result_dict[component] = [sys_package, sa_rpm, 0]
                Display(f"[{component}] is safe by now...", "OK")
    set_value('vulner_info', sa_dict)
    report.cve_result()

def check_fail2ban_client():
    ###判断是否成功安装fail2ban
    ret, result = subprocess.getstatusoutput('fail2ban-client -h')
    if ret == 0:
        #print('fail2ban is installed!')
        pass
    else:
        print('fail2ban is not installed! System exit......')
        sys.exit(1)

    ###判断是否存在jail.local文件， 如果没有则复制一个
    jail_path = '/etc/fail2ban/jail.local'
    if os.path.exists(jail_path):
        #print('jail.local path exists!')
        pass
    else:
        print('Creating jail.local file!')
        ret, result = subprocess.getstatusoutput('cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local')
        if ret == 0:
            print('Creating jail.local successfully!')
        else:
            print('Creating jail.local failed!')
            sys.exit(1)


    ###将cfg文件中的内容写入jail.local文件
    ##读取cfg文件的内容
    #cfg_file_path = '/etc/secScanner/secscanner.cfg'
    jail_content = seconf.get('basic', 'jail_content')
    #jail_content = 'enabled = true\nport = 22\nlogpath = /var/log/secure\nbackend = auto\nbantime = 60m\nfindtime = 1m\nmaxretry = 2\n'
    #print(f'jail_content: {jail_content}')
    with open(jail_path, 'r') as read_file:
        jail_lines = read_file.readlines()
    SSH_WRITE = 0
    with open(jail_path, 'w') as write_file:
        for line in jail_lines:
            if SSH_WRITE == 0:
                write_file.write(line)
                if line == '[sshd]\n':
                    #print("Found [sshd]")
                    SSH_WRITE = 1
                    write_file.write(jail_content)
            else:
                if line == '[dropbear]\n':
                    write_file.write(line)
                    SSH_WRITE = 0
                continue
    ###restart fail2ban-client
    ret, result = subprocess.getstatusoutput('fail2ban-client restart')
    if ret == 0 and result == 'Shutdown successful\nServer ready':
        #print('restart fail2ban-client success!')
        pass
    else:
        print('restart fail2ban-client failed, sys exit!')
        sys.exit(1)

    ###检查systemd中是否设置开机启动服务
    if os.path.exists("/usr/lib/systemd/system/fail2ban_start.service"):
        #print('fail2ban start service exists!')
        pass
    else:
        print('Need to establish fail2ban start service!')

