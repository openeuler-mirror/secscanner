# secscanner部署使用说明

#### 介绍
secScanner是操作系统安全扫描工具，旨在为操作系统提供安全加固、漏洞扫描、rootkit入侵检测等功能。用户可以通过参数配置的定制化方式对系统进行安全方面的扫描检测，在满足系统基线安全加固的同时也可以对用户所选的定制软件包进行漏洞扫描，而系统入侵检测则使用chkrootkit工具。

#### 安装教程
```shell
git clone https://gitee.com/openeuler/secscanner.git
mv secscanner secScanner-1.3
tar -cvf secScanner-1.3.tar.gz secScanner-1.3
cp secScanner-1.3/secscanner.spec rpmbuild/SPECS
rpmbuild -ba rpmbuild/SPECS/secscanner.spec
rpm -ivh secScanner-1.3-x.xxxx.xxxx.noarch.rpm
若提示需安装chkrootkit，则
yum install chkrootkit aide
或相关系统架构的chkrootkit，目前暂无版本要求,如果yum中没有chkrootkit组件，可以从https://pkgs.org/download/chkrootkit中获取rpm包安装或者chkrootkit源码进行编译安装。
```


#### 使用说明
在命令行终端执行“secscanner -h”，显示命令参数提示信息如下：
```shell
usage: secscanner [-h] [--config] [-q] [-V] {useradd,fix,check,restore,db,service} ...

SecScanner command

positional arguments:
  {useradd,fix,check,restore,db,service,ssh}
    useradd             Create a new user to achieve permission separation
    fix                 Fix command
    check               Check command
    restore             Restore command
    db                  Database command
    service             Services command

optional arguments:
  -h, --help            Show this help message and exit
  --config              Show settings file path
  -q, --quiet           Quiet mode
  -V, --version         Show version

Instructions for use:
1、安全检测/加固：secscanner check/fix {basic, euler, level3} 
	  安全检测/加固命令后接参数说明：
      basic：参照《电信网和互联网安全防护基线配置要求及检测要求 操作系统》编写
      euler：参照《openEuler安全配置基线》 编写
      level3：参照《信息安全技术网络安全等级保护基本要求》编写

	  执行效果：通过执行check安全检测，可以检测出系统当前的薄弱项，并记录日志，再次执行fix命令，可以针对系统薄弱项进行安全加固。
      执行安全检测后，检测出满足基线的配置项会输出OK，而针对薄弱项，命令行会输出WARNING警告，提示用户需要进行安全加固。
      执行安全加固后，会根据/etc/secScanner/secscanner.cfg配置文件中设置的参数，对系统进行安全加固。

	  自定义配置：通过/etc/secScanner/secscanner.cfg配置文件，可以针对性设置每一条基线配置项是否进行安全加固。
      各基线配置项存在默认值，根据实际需求设置为【yes】表示启用该项，设置为【no】表示不启用该项。
      cfg文件中配置项说明：
      [basic]：基本安全配置项
          [advance]：高级安全配置项
      [euler]：openEuler安全配置项
      [level3]：网络安全等级保护基本要求配置项

2、配置还原：secscanner restore all
    使用说明：配置还原功能可以将执行安全加固后的配置还原到加固前的状态
        还原原理：执行安全加固时，secScanner会将最初的系统配置文件保存为带 _bak 后缀的备份文件，该文件始终保存最初的配置，此后再进行任何加固行为，备份文件也不会改动。
                执行一键还原后，会检查系统可能加固过的所有_bak备份文件，覆盖掉加固后的配置文件，即系统还原到最初的状态。
        注意：配置还原命令需要输入 y 进行二次确认。系统配置还原后会重启ssh等服务。

3、漏洞扫描：secscanner check {cve, cve_t}
    使用说明：
        secscanner check cve：表示根据当前数据库中的所有漏洞信息，全量扫描整个系统，给出风险组件更新建议。
        secscanner check cve_t：表示根据/etc/secScanner/secscanner.cfg中的[basic]中重点观测组件 rpm_assembly（例如mysql、nginx）进行定向扫描，并给出风险组件更新建议。
        secscanner db update: 从openEuler安全中心拉取漏洞信息保存在本地数据库中，以供漏洞扫描功能。	


4、入侵检测： secscanner check rootkit
	  使用说明：该命令会调用chkrootkit对系统进行入侵检测扫描。

	  执行效果：该命令会调用chkrootkit对系统进行入侵检测扫描，检测出可能存在的rootkit入侵问题信息。
      执行效果中，可能存在的rootkit入侵项会输出WARNING警告，提示用户需要进行相关处理。

5、全量检测：
	  secscanner check all ：一键执行安全检测、漏洞扫描及入侵检测，并提供完整的报告
    HTML报告路径：/var/log/secScanner/html_report

6、定期执行：
	secscanner service {secaide, sechkrootkit} {on, off, status}
	执行secscanner service sechkrootkit on :开启chkrootkit定期扫描，保护系统安全
	执行secscanner service sechkrootkit off :关闭chkrootkit定期扫描
	执行secscanner service sechkrootkit status :查看chkrootkit定期扫描任务状态

```
