# secScanner

#### 介绍
secScanner是操作系统安全扫描工具，旨在为操作系统提供安全加固、漏洞扫描、rootkit入侵检测等功能。用户可以通过参数配置的定制化方式对系统进行安全方面的扫描检测，在满足系统基线安全加固的同时也可以对用户所选的定制软件包进行漏洞扫描，入侵检测扫描使用chkrootkit和secDetector工具。

#### 软件架构
1.系统安全基线配置
- 一键配置：能够一次性的将系统上存在安全弱项的配置进行修改，满足合规要求；
- 配置还原：提供一键化还原配置的功能，确保加固导致系统异常后，能够及时还原到原始状态；
- 自动检测：能够一次性检测当前系统存在的不安全的配置信息；
- 方案提示：未满足安全要求的加固项会通过报告的方式向用户推荐合理的配置步骤；
- 参数控制：所有的加固配置可参数化控制，用户可以自定义是否需要对相关功能点进行配置；

2.系统软件包漏洞检测
- 系统漏洞一键扫描：支持遍历数据库中数据，扫描系统中存在的漏洞；
- 定向检测：支持检测指定的软件包的CVE漏洞，用户可以自行选择需要检测的软件包；
- 内容丰富：软件包漏洞检测需要包括漏洞评分、漏洞修复版本、漏洞状态、缓解方案等信息；
 
3.系统rootkit检测
- 自动检测：能够一次性检测当前系统可能存在的rootkit入侵问题信息；
- 方案提示：对可能的rootkit入侵项进行报告显示和提供相关建议；

4.系统入侵检测和文件完整性扫描服务
- 定时扫描：能够使用chkrootkit和aide定时扫描当前系统；
- 日志可查：使用journalctl查询日志查看是否存在安全问题；

5.报告输出
- 报告输出应包含控制台报告输出、/var/log/xxx.log日志文件输出和html报告输出3大部分；
- 针对系统安全基线的扫描，可将检测结果、加固方案提示等内容以html格式输出相关报告，清晰直观；
- 针对系统软件包漏洞检测，应支持将检测结果以html格式输出相关报告；
- 针对系统rootkit入侵检测，应支持将检测结果以html格式输出相关报告。

#### 安装教程
```shell
git clone https://gitee.com/openeuler/secscanner
mv secscanner secScanner-1.3
tar -cvf secScanner-1.3.tar.gz secScanner-1.3
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
mv secScanner-1.2.tar.gz ~/rpmbuild/SOURCES
cp secScanner-1.3/secscanner.spec ~/rpmbuild/SPECS
rpmbuild -ba ~/rpmbuild/SPECS/secscanner.spec
rpm -ivh ~/rpmbuild/RPMS/xxxx/secScanner-1.3-x.xxxx.xxxx.rpm
若提示需安装chkrootkit和aide，则
yum install chkrootkit aide
或相关系统架构的chkrootkit和aide，目前暂无版本要求
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
安全检测：secscanner check {basic, euler, level3} 
安全加固：secscanner fix {basic, euler, level3} 
	安全检测/加固命令后接参数说明：
		baisc：参照《电信网和互联网安全防护基线配置要求及检测要求 操作系统》编写
		euler：参照《openEuler安全配置基线》 编写
		level3：参照《信息安全技术网络安全等级保护基本要求》编写
	通过执行check安全检测，可以检测出系统当前的薄弱项，并记录日志，再次执行fix命令，可以针对系统薄弱项进行安全加固。
	通过/etc/secScanner/secscanner.cfg配置文件，可以针对性设置每一条基线配置项是否进行安全加固。

漏洞扫描：secscanner check {cve, cve_t}
	使用说明：secscanner check cve表示根据当前数据库中的所有漏洞信息，全量扫描整个系统，给出风险组件更新建议。
		  secscanner check cve_t表示根据/etc/secScanner/secscanner.cfg中的重点观测组件，定向扫描，并给出风险组件更新建议。
	secscanner db update: 从openEuler安全中心拉取漏洞信息，以供漏洞扫描功能。	


入侵检测： secscanner check rootkit
	使用说明：该命令会调用chkrootkit对系统进行入侵检测扫描。

全量检测：
	secscanner check all ：一键执行安全检测、漏洞扫描及入侵检测，并提供完整的报告，路径：/var/log/secScanner/html_report

定期执行：
	secscanner service {secaide, sechkrootkit} {on, off, status}
	执行secscanner service sechkrootkit on :开启chkrootkit定期扫描，保护系统安全
	执行secscanner service sechkrootkit off :关闭chkrootkit定期扫描
	执行secscanner service sechkrootkit status :查看chkrootkit定期扫描任务状态

```

#### 参与贡献
1.Fork本仓库
2.当前快速迭代期间，仅master分支，因此只需在master做变更后提交
3.创建pr，描述清楚pr的具体功能、作用
4.通知仓库maintainer审核pr

