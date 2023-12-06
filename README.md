# secscanner

#### 介绍
secScanner是操作系统安全扫描工具，旨在为操作系统提供安全加固、漏洞扫描、rootkit入侵检测等功能。用户可以通过参数配置的定制化方式对系统进行安全方面的扫描检测，在满足系统基线安全加固的同时也可以对用户所选的定制软件包进行漏洞扫描，而系统入侵检测则使用chkrootkit工具。

#### 软件架构
- 1.  系统安全基线配置：一键配置：能够一次性的将系统上存在安全弱项的配置进行修改，满足合规要求；配置还原：提供一键化还原配置的功能，确保加固导致系统异常后，能够及时还原的原始状态；自动检测：能够一次性检测当前系统存在的不安全的配置信息；方案提示：未满足安全要求的加固项会通过报告的方式向用户推荐合理的配置步骤；参数控制：所有的加固配置可参数化控制，用户可以自定义是否需要对相关功能点进行配置；
- 2.  系统软件包漏洞检测，此模块又细分如下的几个功能点，包括：系统漏洞一键扫描：支持遍历数据库中数据，扫描系统中存在的漏洞；定向检测：支持检测指定的软件包的CVE漏洞，用户可以自行选择需要检测的软件包；内容丰富：软件包漏洞检测需要包括漏洞评分、漏洞修复版本、漏洞状态、缓解方案等信息； 
- 3.  系统rootkit检测，此模块又细分以下几个功能点，包括：自动检测：能够一次性检测当前系统可能存在的rootkit入侵问题信息；方案提示：对可能的rootkit入侵项进行报告显示和提供相关建议；
- 4.  报告输出报告输出应包含控制台报告输出、/var/log/xxx.log日志文件输出和html报告输出3大部分；针对系统安全基线的扫描，可将检测结果、加固方案提示等内容以html格式输出相关报告，清晰直观；
针对系统软件包漏洞检测，应支持将检测结果以html格式输出相关报告；针对系统rootkit入侵检测，应支持将检测结果以html格式输出相关报告。

#### 安装教程
```shell
git clone https://gitee.com/openeuler/secscanner
mv secscanner secscanner-0.1
tar -cvf secScanner-0.1.tar.gz secscanner-0.1
cp secscanner-0.1/secscanner.spec rpmbuild/SPECS
rpmbuild -ba rpmbuild/SPECS/secscanner.spec
rpm -ivh secScanner-1.0-0.xxxx.xxxx.noarch.rpm
若提示需安装chkrootkit，则
yum install chkrootkit
或相关系统架构的chkrootkit，版本目前无要求
```

#### 使用说明
在命令行终端执行“secscanner -h”命令，显示命令参数提示信息，具体显示如下所示：
```shell
usage: secscanner [-h] [--config] [-q] [-V] {auto,fix,check,restore,db,vulner} ...

SecScanner command

positional arguments:
  {auto,fix,check,restore,db,vulner}
    auto                auto command
    fix                 Fix command
    check               Check command
    restore             Restore command
    db                  Database command
    vulner              Scan vulner command

optional arguments:
  -h, --help            show this help message and exit
  --config              Show settings file path
  -q, --quiet           Quiet mode
  -V, --version         Show version
```

#### 参与贡献
1.  Fork 本仓库
2.  当前快速迭代期间，仅 master 分支，因此您只需在 master 做变更后提交
3.  创建 pr ，描述清楚 pr 的具体功能、作用
4.  通知仓库 maintainer 审核 pr

