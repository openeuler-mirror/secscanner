# secscanner

#### introduce

secScanner is an operating system security scanning tool designed to provide  security hardening, vulnerability scanning, rootkit intrusion detection, and other functions for the operating system. Users can scan and detect the security aspects of the system through customized parameter  configurations, and at the same time meet the security hardening of the  system baseline and scan the vulnerabilities of the customized software  packages selected by the user, and the system intrusion detection uses  the chkrootkit tool. 

#### Software Architecture
1. Configure the system security baseline 

- One-click configuration: The configuration with security weaknesses on the system can be modified at one time to meet compliance requirements. 
- Configuration restoration: provides a one-click configuration restoration function to ensure that the original state can be restored in time after the system is abnormal. 
- Automatic detection: It can detect the insecure configuration information of the current system at one time; 
- Solution tip: Reinforcement items that do not meet security requirements will be reported to recommend reasonable configuration steps to users. 
- Parameter control: All reinforcement configurations can be parameterized, and  users can customize whether they need to configure relevant function  points; 

2. System package vulnerability detection 

- One-click scanning of system vulnerabilities: supports traversing data in the  database to scan for vulnerabilities in the system; 
- Targeted detection: You can detect CVE vulnerabilities in specified software  packages, and you can select the software packages you want to detect. 
- Rich content: Software package vulnerability detection needs to include  information such as vulnerability score, vulnerability fix version,  vulnerability status, and mitigation plan. 

3. System rootkit detection 

- Automatic detection: It can detect possible rootkit intrusion information in the current system at one time; 
- Solution tip: Report and display possible rootkit intrusions and provide relevant suggestions; 

4. Report output 

- The report output should include three parts: console report output, /var/log/xxx .log log file output, and html report output; 
- For the scanning of system security baselines, the detection results,  hardening solution prompts, and other content can be output in HTML  format, which is clear and intuitive. 
- For system package vulnerability detection, the detection results should be output in HTML format. 
- For system rootkit intrusion detection, you can output the detection results in HTML format. 

#### Installation tutorial

```
git clone https://gitee.com/openeuler/secscanner
mv secscanner secScanner-0.1
tar -cvf secScanner-0.1.tar.gz secScanner-0.1
cp secScanner-0.1/secscanner.spec rpmbuild/SPECS
rpmbuild -ba rpmbuild/SPECS/secscanner.spec
rpm -ivh secScanner-1.0-0.xxxx.xxxx.noarch.rpm
若提示需安装chkrootkit，则
yum install chkrootkit
或相关系统架构的chkrootkit，目前暂无版本要求
```

#### Directions for use

Run the secscanner -h command in the CLI terminal to display the following parameter prompts: 

```
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


#### Gitee involved

1.Fork this repository

 2.During the current rapid iteration, only the master  branch, so you only need to submit it after the master makes changes  

3.Create a PR and describe the specific functions and functions of the  PR 

4.Notify the repository maintainer to review the PR
