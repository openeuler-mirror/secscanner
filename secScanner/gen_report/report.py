from secScanner.gconfig import *
import logging
import subprocess
import re
import os
import shutil
import itertools
import secScanner.gen_report.gen_html_report as gen_report

logger = logging.getLogger('secscanner')


def warning_results():

    def show_warnings():
        print("")
        print(f"{OK}BaseLine Warnings{NORMAL}")
        print(f"{WHITE}----------------------------{NORMAL}")
        WRNS = []
        SUGS = []
        baseline_info = ""

        with open(LOGFILE, "r") as file:
            lines = file.readlines()

        for line in lines:
            wrn_match = re.search(r'WRN_C\d{2}(_\d{2})?:', line)
            suggestion_match = re.search(r'SUG_C\d{2}(_\d{2})?:', line)

            if wrn_match:
                wrn = line.split(wrn_match.group(0))[1].strip()
                WRNS.append(wrn)
            if suggestion_match:
                sug = line.split(suggestion_match.group(0))[1].strip()
                SUGS.append(sug)            

        TMP_COUNT = 0

        for wrn, sug in itertools.zip_longest(WRNS, SUGS, fillvalue=""):
            print(f"{RED}- {wrn} {NORMAL}")
            TMP_COUNT += 1
            baseline_info += f"""
                <tr style="cursor:pointer; border:solid 1px #ddd;">
                <td>{TMP_COUNT}</td>
                <!--   <td>用户权限</td>  -->
                <td>{wrn}</span></td>
                <td>{sug}</td>
                </tr>
            """
        set_value("baseline_info", baseline_info)
        TOTAL_WARNINGS = TMP_COUNT
        set_value("TOTAL_WARNINGS", TOTAL_WARNINGS)
        
        if TOTAL_WARNINGS ==0:
            print("NO warnings")
            print("")

        return baseline_info

    #QUIET = get_value("QUIET")
    if QUIET == 0:
        print("")
        print("=" * 81)
        print("")
        print(f"  -[ {WHITE}{PROGRAM_NAME} {PROGRAM_VERSION} Results{NORMAL} ]-")
        print("")
        print("-" * 67)
        show_warnings()


def rootkit_result():
    rootkit_info = ""
    html_rootkit_content = ""

    with open(LOGFILE, 'r') as file:
        lines = file.readlines()

        infected_count = 0
        infected_list = []

        for line in lines:
            if "INFECTED" in line:
                infected_count += 1
                infected_list.append(line.strip())

        if infected_count > 0:
            rootkit_info += f"INFECTED ({infected_count}):\n"
            rootkit_info += "----------------------------\n"
            rootkit_info += "\n".join(infected_list) + "\n"
        else:
            rootkit_info += "No INFECTED\n"
        print(rootkit_info)

        for index, infected_line in enumerate(infected_list):
            suggestion = "请重新检查问题文件，或删除病毒文件，或重装系统"
            html_rootkit_content += f"""
            <tr style="cursor:pointer; border:solid 1px #ddd;">
            <td>{index + 1}</td>
            <!--
            <td><font color="red">{infected_line}</font></td>
            <td>{suggestion}</td>
            </tr>
            """
    set_value("html_rootkit_content", html_rootkit_content)
    TOTAL_INFECTED = infected_count
    set_value("TOTAL_INFECTED", TOTAL_INFECTED)

    return html_rootkit_content

def cve_result():
    # init database to get more cve info
    engine = create_engine('sqlite:///secScanner/db/cvedatabase.db', echo=False)
    DBModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # get cveId by saId
    sa_dict = get_value('vulner_info')

    vulne_info = ""
    cve_count = 0
    cve_list = []
    if sa_dict == {}:
        set_value("vulne_info", vulne_info)
        TOTAL_CVES = 0
        set_value("TOTAL_CVES", TOTAL_CVES)
        vulne_info += "No vulnerabilities\n"
        return vulne_info
    for single_sa in sa_dict:
        for single_data in sa_dict[single_sa][0]:
            temp = []
            temp.append(single_data)
            cve_sample = session.query(CVE).filter_by(cveId=f'{single_data}', packageName=f'{sa_dict[single_sa][1]}').first()
            temp.append(cve_sample.packageName)
            temp.append(sa_dict[single_sa][2])
            temp.append(cve_sample.cvsssCoreOE)
            temp.append(cve_sample.attackVectorOE)
            temp.append(cve_sample.attackComplexityOE)
            temp.append(single_sa)
            temp.append(cve_sample.summary)
            cve_list.append(temp)
            cve_count += 1
    gen_cve_json_file(cve_list)
    cve_report_max_items = 0
    # add cve info

    vulne_info += f"Vulnerabilities Details ({cve_count}):\n"
    vulne_info += "----------------------------\n"

    for i in range(len(cve_list)):
        if i + 1 <= 1000:
            vulne_info += f"  <tr style=\"cursor:pointer; border:solid 1px \#ddd;\">"
            vulne_info += f"    <td>{i+1}</td>\n"
            vulne_info += f"    <td>{cve_list[i][0]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][1]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][2]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][3]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][4]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][5]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][6]}</td>\n"
            vulne_info += f"    <td>{cve_list[i][7]}</td>\n"
            vulne_info += f"  </tr>\n"

        else:
            if cve_report_max_items == 0:  # 判断是否是第一次超过最大项数
                vulne_info += "This system has more than 10000 CVEs, skip output too much info on shell console. You can see html report for details.\n"
                vulne_info += "Also you can change the max cve output count:cve_report_max_items={} in {}.txt, and rerun the program to see all cve info.\n".format(
                    len(cve_list), '.bash_profile')
                cve_report_max_items = 1
    vulne_info += "</table>\n"
    set_value("vulne_info", vulne_info)
    TOTAL_CVES = cve_count
    set_value("TOTAL_CVES", TOTAL_CVES)
    return vulne_info

def main():

    warning_results()
    rootkit_result()
    cve_result()
    HTML_REPORT_DIRNAME = "html_report"
    set_value("HTML_REPORT_DIRNAME",HTML_REPORT_DIRNAME)
    html_report_dir = os.path.join(LOGDIR, HTML_REPORT_DIRNAME)
    if os.path.exists(html_report_dir):
        shutil.rmtree(html_report_dir)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # target_file
    target_file = os.path.join(current_dir, 'result_template')


    #os.makedirs(html_report_dir)
    shutil.copytree(target_file, html_report_dir)


    gen_report.gen_html_report()
