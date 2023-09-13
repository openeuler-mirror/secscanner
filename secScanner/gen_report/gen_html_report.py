import re
import socket
import psutil

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address
from secScanner.gconfig import *
def gen_html_report():
    HTML_REPORT_DIRNAME = get_value("HTML_REPORT_DIRNAME")
    report_datetime_start = get_value("report_datetime_start")
    report_datetime_end = get_value("report_datetime_end")
    HOSTNAME = get_value("HOSTNAME")
    MY_IP = get_ip_address()
    users = psutil.users()
    USER = users[0].name
    OS_KERNELVERSION_FULL = get_value("OS_KERNELVERSION_FULL")
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    baseline_info = get_value("baseline_info")
    TOTAL_WARNINGS = get_value("TOTAL_WARNINGS")
    vulne_info = get_value("vulne_info")
    TOTAL_CVES = get_value("TOTAL_CVES")
    html_rootkit_content = get_value("html_rootkit_content")
    TOTAL_INFECTED = get_value("TOTAL_INFECTED")

    with open(f"{LOGDIR}/{HTML_REPORT_DIRNAME}/index.html", "w") as f:
        f.write(f'''
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="generator"
        content="HTML Tidy for HTML5 (experimental) for Windows https://github.com/w3c/tidy-html5/tree/c63cc39" />
        <meta http-equiv="Content-Type" content="text/html" charset="utf-8" />
        <title>系统安全评估报告</title>
        <link rel="stylesheet" href="reportfiles/css/ns_report.css" />
        <link rel="stylesheet" href="reportfiles/css/ns_report_rsas.css" />
        <link rel="stylesheet" href="reportfiles/js/datepicker/skin/WdatePicker.css" />
        <script src="reportfiles/js/jquery.js"></script>
        <script src="reportfiles/js/common.js"></script>
        <script src="reportfiles/js/datepicker/WdatePicker.js"></script>
      </head>
      <body>
        <div id="report" class="wrapper_w800">
          <div class="report_tip"></div>
          <div id="head" class="report_title">
            <h1>&quot;系统&quot;安全评估报告</h1>
          </div>
          <!--head end,catalog start-->
          <div id="catalog">
            <div class="report_h1">目录</div>
          </div>
          <div id="content">
            <div class="report_h report_h1">1.综述信息</div>
            <div class="report_content">
              <div class="report_h report_h2" id="title01">1.1任务信息</div>
              <div>
                <table width="100%">
                  <tr>
                    <td width="50%" valign='top'>
                      <table class="report_table plumb">
                        <tbody>
                          <tr class="odd">
                            <th width="120">任务名称</th>
                            <td> 系统安全评估报告 </td>
                          </tr>
                          <tr class="even">
                            <th>任务类型</th>
                            <td>基线检查与常规软件漏洞扫描</td>
                          </tr>
                          <tr class="odd">
                            <th width="120">任务状态</th>
                            <td>扫描完成</td>
                          </tr>
                          <tr class="even">
                            <th>漏洞扫描模板</th>
                            <td>系统基线配置与常规软件漏扫</td>
                          </tr>
                          <tr class="odd">
                            <th>下达任务用户</th>
                            <td>{USER}</td>
                          </tr>
                          <tr class="even">
                            <th>任务数据来源</th>
                            <td>本地扫描</td>
                          </tr>
                          <tr class="odd">
                            <th>任务说明</th>
                            <td>系统安全分析工具</td>
                          </tr>
                        </tbody>
                      </table>
                        </td>
                        <td width="20px"></td>
                        <td width="50%" valign='top'>
                          <table class="report_table plumb">
                            <tbody>
                              <tr class="odd">
                                <th width="120px">时间统计</th>
                                <td>开始：{report_datetime_start}
                                <br />结束：{report_datetime_end}</td>
                              </tr>
                              <tr class="even">
                                <th>主机信息</th>
                                <td>HOSTNAME：{HOSTNAME}
                                <br />IP：{MY_IP}
                                <br />USER：{USER}
                                <br />内核版本：{OS_KERNELVERSION_FULL}</td>
                              </tr>
                              <tr class="odd">
                                <th>扫描工具版本信息</th>
                                <td>{PROGRAM_NAME} - {PROGRAM_VERSION}</td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </div>
                </div>
                <div class="report_h report_h1">2.风险类别</div>
                <div class="report_content">
                  <div class="report_h report_h2" id="vuln_risk_category">2.1 系统基线安全</div>
                  <div>
                    <table class="report_table plumb">
                      <thead>
                        <tr class="first_title">
                          <td width="30px">序号</td>
        <!--              <td width="60px">功能模块</td>  -->
                          <td width="260px">加固问题项</td>
                          <td>修复意见</td>
                        </tr>
                      </thead>
                      <tbody>
                        {baseline_info}
        <!--                <tr style="cursor:pointer;" class="odd">
                          <td>1</td>
                          <td>用户权限</td>
                          <td>
                          <span class="font_high"> No password minlenset, please check</span>
                          </td>
                          <td>
                            echo "xxx" /etc/pam.d/system-auth
                          </td>
                        </tr>
        -->
                      </tbody>
                      <tfoot>
                        <tr class="second_title">
                          <td colspan="2">合计</td>
                          <td>
                            <span class="font_high">{TOTAL_WARNINGS}</span>
                          </td>
                        </tr>
                      </tfoot>

                    </table>
                  </div>
                  <br />
                  <div class="report_h report_h2" id="title00">2.2 系统漏洞分布</div>
                  <div>
        <!--            <div style="text-align:rightvertical-align:middle;">漏洞类别：
                    <img align="absbottom" src="reportfiles/images/vuln_high.gif" />高风险[3]
                    <img align="absbottom" src="reportfiles/images/vuln_middle.gif" />中危险[7]
                    <img align="absbottom" src="reportfiles/images/vuln_low.gif" />低风险[10]</div>
        -->
                    <table class="report_table plumb">
                      <thead>
                        <tr class="first_title">
                          <td style='width:30px'>序号</td>
                          <td style='width:50px'>CVE号</td>
                          <td style='width:50px'>涉及软件包名</td>
                          <td style='width:50px'>漏洞修复版本</td>
                          <td style='width:25px'>漏洞评分</td>
                          <td style='width:25px'>利用方式</td>
                          <td style='width:40px'>利用复杂度</td>
                          <td style='width:40px'>RHSA</td>
                          <td >CVE漏洞描述</td>
                        </tr>
                      </thead>
                      <tbody>
                        {vulne_info}
                      </tbody>
                    <tfoot>
                <tr class="first_title">
                  <td colspan="8">合计</td>
                  <td>
                      <span class="font_high">{TOTAL_CVES}</span>
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
        <div class="report_h report_h1">3.主机信息</div>
        <div class="report_content">
          <div class="report_h report_h2" id="title02">3.1主机风险等级列表</div>
          <div>
            <table class="report_table plumb">
              <thead>
                <tr class="first_title">
                  <td width="130px">IP地址</td>
                  <td>主机名</td>
                  <td>操作系统</td>
                  <!-- td colspan="4" width="40px">漏洞风险（个）</td -->
                  <th width="190px" style="white-space:pre-wrap;">内核版本</th>
                </tr>
              </thead>
              <tbody>
                <tr style="cursor:pointer;" class="odd">
                  <td>{MY_IP}</td>
                  <td>{HOSTNAME}</td>
                  <td>{OS_ID} {OS_DISTRO}</td>
                  <td>{OS_KERNELVERSION_FULL}</td>
                </tr>
              </tbody>
              <!--                <tfoot>
                  <tr class="second_title">
                    <td colspan="3">合计</td>
                    <td>
                      <span class="font_high">12</span>
                    </td>
                    <td>28</td>
                    <td>37</td>
                    <td>77</td>
                    <td>9.3</td>
                  </tr>
                </tfoot>
-->
            </table>
          </div>
        </div>
        <div class="report_h report_h1">4.入侵检测信息</div>
        <div class="report_content">
          <div class="report_h report_h2" id="title03">4.1入侵检测列表</div>
          <div>
            <table class="report_table plumb">
              <thead>
                 <tr class="first_title">
                   <td width="30px">序号</td>
                   <td width="400px">入侵检测项</td>
                   <td>检测结果或建议</td>
                 </tr>
               </thead>
               <tbody>
                 {html_rootkit_content}
               </tbody>
               <tfoot>
                 <tr class="second_title">
                   <td colspan="2">可疑问题项合计</td>
                   <td>
                     <span class="font_high">{TOTAL_INFECTED}</span>
                   </td>
                 </tr>
               </tfoot>
             </table>
            </div>
           </div>
        </div>
       </div>
    </body>
</html>
''')

