# secscanner

#### introduce

secScanner is an operating system security scanning tool designed to provide security reinforcement, vulnerability scanning, rootkit intrusion detection, and other functions for operating systems. Users can perform security scanning and detection on the system through customized parameter configuration. While meeting the requirements of system baseline security reinforcement, users can also scan for vulnerabilities in the customized software packages they have selected. Intrusion detection scanning uses chkrootkit and secDetector tools.

#### Software Architecture
1. System security baseline configuration 

-One click configuration: capable of modifying configurations with security vulnerabilities on the system at once to meet compliance requirements; 
-Configuration restoration: Provides a one click restoration function for configuration, ensuring that the original state can be restored in a timely manner after system anomalies caused by reinforcement; 
-Automatic detection: capable of detecting unsafe configuration information in the current system at once; 
-Solution tip: Reinforcement items that do not meet security requirements will be recommended to users through a report with reasonable configuration steps; 
-Parameter control: All reinforcement configurations can be parameterized and controlled, and users can customize whether to configure relevant functional points; 

2. System software package vulnerability detection 

-One click system vulnerability scanning: supports traversing data in the database and scanning for vulnerabilities in the system; 
-Targeted detection: supports detecting CVE vulnerabilities in specified software packages, and users can choose the software packages they need to detect; 
-Rich content: Software package vulnerability detection requires information such as vulnerability rating, vulnerability repair version, vulnerability status, mitigation plan, etc; 

3. System rootkit detection 

-Automatic detection: capable of detecting possible rootkit intrusion issues in the current system at once; 
-Solution tip: Report and display possible rootkit intrusions, and provide relevant suggestions; 

4. System intrusion detection and file integrity scanning services 

-Timed scanning: Can use chkrootkit and aide to scan the current system at regular intervals; 
-Log check: Use Journalctl to query the logs and check for any security issues; 

5. Report output 

-The report output should include three main parts: console report output,/var/log/xx.log log log file output, and HTML report output; 
-For the scanning of system security baselines, relevant reports such as detection results and reinforcement plan prompts can be output in HTML format, which is clear and intuitive; 
-For system software package vulnerability detection, it should support outputting relevant reports in HTML format based on the detection results; 
-For system rootkit intrusion detection, it should support outputting relevant reports in HTML format based on the detection results.

#### Installation tutorial

```
git clone https://gitee.com/openeuler/secscanner
mv secscanner secScanner-1.2
tar -cvf secScanner-1.2.tar.gz secScanner-1.2
cp secScanner-1.2/secscanner.spec rpmbuild/SPECS
rpmbuild -ba rpmbuild/SPECS/secscanner.spec
rpm -ivh rpmbuild/RPMS/xxxarch/secScanner-1.2.0.xxxx.xxxxrpm
if need to install chkrootkit，then
yum install chkrootkit
```

#### Directions for use

Run the secscanner -h command in the CLI terminal to display the following parameter prompts: 

```
usage: secscanner [-h] [--config] [-q] [-V] {useradd,fix,check,restore,db,service,ssh} ...

SecScanner command

positional arguments:
  {useradd,fix,check,restore,db,service,ssh}
    useradd             Create a new user to achieve permission separation
    fix                 Fix command
    check               Check command
    restore             Restore command
    db                  Database command
    service             Services command
    ssh                 SSH ban&unban command

optional arguments:
  -h, --help            Show this help message and exit
  --config              Show settings file path
  -q, --quiet           Quiet mode
  -V, --version         Show version

```


#### Gitee involved

1.Fork this repository

2.During the current rapid iteration, only the master  branch, so you only need to submit it after the master makes changes  

3.Create a PR and describe the specific functions and functions of the  PR 

4.Notify the repository maintainer to review the PR
