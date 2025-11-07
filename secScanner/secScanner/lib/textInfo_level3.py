# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, 
   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, 
   MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''

# level3 warning
WRN_C111_01 = "There is an empty password user present"
WRN_C111_02 = "file /etc/shadow not exists"

WRN_C112_01 = "There are duplicate UIDs present"
WRN_C112_02 = "Failed to retrieve users for UID"
WRN_C112_03 = "Failed to retrieve UID information"
WRN_C112_04 = "file /etc/passwd not exists"

WRN_C113_01 = "There are duplicate GIDs present"
WRN_C113_02 = "Failed to retrieve GID information"
WRN_C113_03 = "file /etc/group not exists"

WRN_C114_01 = "PASS_MAX_DAYS value is not safe"
WRN_C114_02 = "PASS_MAX_DAYS value is null"
WRN_C114_03 = "PASS_MIN_DAYS value is not safe"
WRN_C114_04 = "PASS_MIN_DAYS value is null"
WRN_C114_05 = "PASS_MIN_LEN value is not safe"
WRN_C114_06 = "PASS_MIN_LEN value is null"
WRN_C114_07 = "PASS_WARN_AGE value is not safe"
WRN_C114_08 = "PASS_WARN_AGE value is null"

WRN_C115_01 = "Wrong password minLen set"
WRN_C115_02 = "No password minLen set"
WRN_C115_03 = "Wrong password minclass set"
WRN_C115_04 = "No password minclass set"
WRN_C115_05 = "Wrong Password ucredit set"
WRN_C115_06 = "No password ucredit set"
WRN_C115_07 = "Wrong password lcredit set"
WRN_C115_08 = "No password lcredit set"
WRN_C115_09 = "wrong Password dcredit set"
WRN_C115_10 = "No Password dcredit set"
WRN_C115_11 = "wrong Password ocredit set"
WRN_C115_12 = "No Password ocredit set"
WRN_C115_13 = "No enforce for root set"


WRN_C121_01 = "wrong user login lock Deny set"
WRN_C121_02 = "No user login lock Deny set"

WRN_C122_01 = "Wrong ssh login timeout set"
WRN_C122_02 = "No ssh login timeout set"
WRN_C122_03 = "SSH login connection timeout configuration issue"
WRN_C122_04 = "file /etc/ssh/sshd_config does not exist"

WRN_C123_01 = "No TMOUT set, and this not safe"
WRN_C123_02 = "Wrong TMOUT set, and this not safe"

WRN_C131_01 = "The SSH service is not running"
WRN_C131_02 = "Failed to check if the service is available"
WRN_C131_03 = "file /usr/lib/systemd/system/sshd.service does not exist"

WRN_C132 = "Telnet enabled, need to disable"

WRN_C133_01 = "HTTP not removed"
WRN_C133_02 = "Query command execution failed"

WRN_C134_01 = "TFTP not removed"
WRN_C134_02 = "Query command execution failed"

WRN_C135_01 = "No Protocol set"
WRN_C135_02 = "file /etc/ssh/sshd_config does not exist"

WRN_C213 = "Umask value is not 027, need change for secure"

WRN_C211_01 = "There are users with UID 0 who are not root"
WRN_C211_02 = "Failed to obtain information with UID 0"
WRN_C211_03 = "file /etc/passwd does not exist"

WRN_C212_01 = "At least one password has expired"
WRN_C212_02 = "file /etc/shadow dose not exist"

WRN_C221_01 = "No ssh Root Deny setting, need add"
WRN_C221_02 = "Wrong ssh Root Deny setting"

WRN_C222 = "Has unused user need to be disabled"

WRN_C231_01 = "At least one account has expired"
WRN_C231_02 = "file /etc/shadow dose not exist"

WRN_C241 = "There is no pam_wheel set"

WRN_C251 = "Check /etc/passwd property is not 644"

WRN_C252 = "Check /etc/shadow property is not 400"

WRN_C253 = "Check /etc/group property is not 644"

WRN_C254 = "Check /etc/gshadow property is not 0"

WRN_C255 = "Check /etc/passwd- property is not 644"

WRN_C256 = "Check /etc/shadow- property is not 400"

WRN_C257 = "Check /etc/group- property is not 644"

WRN_C258 = "Check /etc/gshadow- property is not 0"

WRN_C259 = "Wrong ssh key file permission set"

WRN_C271 = "Wrong selinux set"

WRN_C311_01 = "Wrong auditd service status"
WRN_C311_02 = "No auditd service"

WRN_C312_01 = "Wrong rsyslog service status"
WRN_C312_02 = "No rsyslog service"

WRN_C320 = "Wrong audit rules set"

WRN_C331 = "No audit.conf max_log_file_action set"

WRN_C332 = "No audit.conf space_left_action、action_mail_acct、admin_space_left_action set"

WRN_C411 = "The FTP software is installed in your Linux System"

WRN_C412 = "The Kexec-tools software is installed in your Linux System"

WRN_C413 = "The Ypbind software is installed in your Linux System "

WRN_C415 = "Don't have aide installed"

WRN_C416 = "Don't have chrony installed"

WRN_C421 = "The nfs-Server is enabled in your Linux System "

WRN_C422 = "The DNS server is enabled in your Linux System "

WRN_C423 = "Wrong dhcp service status"

WRN_C424 = "Wrong RPC service status"

WRN_C425 = "Wrong samba service status"

WRN_C426 = "Wrong snmpd service status"

WRN_C427 = "Wrong IMAP and POP3 service status"

WRN_C428 = "Wrong ntalk service status"

WRN_C429 = "Wrong rsh.socket service status"
WRN_C1021 = "Wrong HISTSIZE set in /etc/profile"

#level3 suggestion
SUG_C111_01 = ("1、执行备份："
               "</br>#cp -np /etc/shadow /etc/shadow_bak"
               "</br>执行awk -F: '($2 == \"\") { print $1}' /etc/shadow "
               "</br>若存在输出，则将输出的用户名锁定"
               "</br>使用passwd -l username 锁定用户")
SUG_C111_02 = ("请检查系统是否存在文件/etc/shadow")
SUG_C112_01 = ("1、执行备份："
               "</br>#cp -np /etc/passwd /etc/passwd_bak"
               "</br>将重复UID的用户使用userdel删除")
SUG_C112_02 = ("该指令 awk -F: '$3 == \"{uid}\" {{ print $1 }}' /etc/passwd 执行失败")
SUG_C112_03 = ("该指令 cut -f3 -d: /etc/passwd | sort -n | uniq -c 执行失败")
SUG_C112_04 = ("请检查系统是否存在文件 /etc/passwd")
SUG_C113_01 = ("1、执行备份："
               "</br>#cp -np /etc/group /etc/group"
               "</br>进入文件，将重复GID根据需求删除"
               "</br>保存退出")
SUG_C113_02 = ("该指令 cut -d: -f3 /etc/group | sort | uniq -d 执行失败")
SUG_C113_03 = ("请检查系统是否存在文件 /etc/group")
SUG_C114_01 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_MAX_DAYS 90，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_MAX_DAYS值不大于90")
SUG_C114_02 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_MIN_DAYS 6，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_MIN_DAYS值不小于6")
SUG_C114_03 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_MIN_LEN 8，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_MIN_LEN值不小于8")
SUG_C114_04 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_WARN_AGE 30，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_WARN_AGE值不小于30")
SUG_C115_01 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... minlen=8 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C115_02 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... minclass=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C115_03 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... ucredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C115_04 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... lcredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C115_05 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth "
               "</br>password    requisite     pam_pwquality.so ... dcredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C115_06 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... ocredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C115_07 = ("1、执行备份："
              "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth "
              "</br>password    requisite     pam_pwquality.so ... enforce_for_root ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C121 = ("1、执行备份："
            "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
            "</br>#cp -np /etc/pam.d/password-auth /etc/pam.d/password-auth_bak "
            "</br>2、修改策略设置："
            "</br>#vi /etc/pam.d/system-auth"
            "</br>#vi /etc/pam.d/password-auth"
            "</br>增加auth required pam_tally2.so deny=5 onerr=fail unlock_time=300到第二行，保存退出；"
            "</br>补充操作说明：使配置生效需重启服务器。"
            "</br>root帐户不在锁定范围内。"
            "</br>若需锁定root，则再deny后添加even_deny_root"
            "</br>帐户被锁定后，可使用faillog -u <username> -r或pam_tally2 --user <username> --reset解>锁。"
            "</br>/etc/pam.d/system-auth和/etc/pam.d/password-auth文件中存在deny的值小于等于5")
SUG_C122_01 = ("1、执行备份："
               "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak"
               "</br>2、修改配置文件："
               "</br>#vi /etc/ssh/sshd_config"
               "</br>将ClientAliveInterval取消注释并修改值为900(建议0<val<=900)"
               "</br>将ClientAliveCountMax取消注释并修改值为0"
               "</br>保存退出")
SUG_C122_02 = ("/etc/ssh/sshd_config 文件不存在，请检查系统")
SUG_C123 = ("1、执行备份："
            "</br>#cp -np /etc/profile /etc/profile_bak "
            "</br>#cp -np /etc/csh.cshrc /etc/csh.cshrc_bak "
            "</br>2、在/etc/profile文件增加以下两行："
            "</br>#vi /etc/profile "
            "</br>TMOUT=180 "
            "</br>export TMOUT "
            "</br>3、修改/etc/csh.cshrc文件，添加如下行："
            "</br>set autologout=30 "
            "</br>改变这项设置后，重新登录才能有效。 "
            "</br>补充操作说明：/etc/profile 文件中TMOUT值小于等于600 "
            "</br>或者/etc/csh.cshrc文件中autologout小于等于600")
SUG_C131_01 = ("使用systemctl status sshd 查看服务状态"
               "</br>尝试使用systemctl start sshd 开启服务"
               "</br>若不成则查看日志定位错误或联系技术人员处理")
SUG_C131_02 = ("systemctl is-active sshd 指令执行失败"
               "</br>手动执行指令查看是否失败，若失败则联系技术人员")
SUG_C131_03 = ("/usr/lib/systemd/system/sshd.service 文件不存在"
               "</br>rpm -qa openssh 查看是否安装sshd服务")
SUG_C132 = ("netstat -tln | grep \':23\'查看是否存在telnet开启端口"
            "</br>若存在，则需要停止服务并且禁用"
            "</br>使用systemctl stop telnet.socket停止服务"
            "</br>systemctl is-enabled telnet.socket查看是否使能"
            "</br>若已使能，使用systemctl disable telnet.socket禁用")
SUG_C133_01 = ("执行yum remove httpd -y 移除httpd包")
SUG_C133_02 = ("手动执行rpm -qa httpd* 查看是否存在"
               "</br>若存在则执行yum remove httpd -y移除")
SUG_C134_01 = ("执行yum remove tftp -y 移除tftp包")
SUG_C134_02 = ("手动执行rpm -qa tftp* 查看是否存在"
               "</br>若存在则执行yum remove tftp -y移除")
SUG_C135_01 = ("1、执行备份："
               "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak"
               "</br>2、配置ssh协议"
               "</br>#vi /etc/ssh/sshd_config"
               "</br>新增或修改为 Protocol 2，保存退出")
SUG_C135_02 = ("文件 /etc/ssh/sshd_config 不存在，请查看是否已安装openssh包")
SUG_C213 = ("1、执行备份："
            "</br>#cp -np /etc/profile /etc/profile_bak "
            "</br>#cp -np /etc/csh.login /etc/csh.login_bak "
            "</br>#cp -np /etc/csh.cshrc /etc/csh.cshrc_bak "
            "</br>#cp -np /etc/bashrc /etc/bashrc_bak "
            "</br>#cp -np /root/.bashrc /root/.bashrc_bak "
            "</br>#cp -np /root/.cshrc /root/.cshrc_bak "
            "</br>2、修改umask设置："
            "</br>将以上文件的umask值修改为027，保存退出。"
            "</br>补充操作说明：umask设置不当可能导致某些应用无法正确自动创建目录或文件，从而运行异常。"
            "</br>/etc/profile 文件中umask值大于等于027")
SUG_C211_01 = ("1、执行备份："
               "</br>#cp -np /etc/passwd /etc/passwd_bak"
               "</br>#vi /etc/passwd"
               "</br>查看第三位是否存在除root以外为0的用户"
               "</br>若存在，修改该文件或userdel 删除用户")
SUG_C211_02 = ("1、执行备份："
               "</br>#cp -np /etc/passwd /etc/passwd_bak"
               "</br> awk -F: '($3 == 0) { print $1 }' /etc/passwd 该指令执行失败"
               "</br>手动执行上述指令，查看是否存在报错"
               "</br>若存在则联系技术人员解决")
SUG_C211_03 = ("文件 /etc/passwd，请检查系统是否运行正常")
SUG_C212_01 = ("1、执行备份："
               "</br>#cp -np /etc/shadow /etc/shadow_bak"
               "userdel username 删除密码已过期的用户或passwd username 修改密码")
SUG_C212_02 = ("文件 /etc/shadow 不存在，请检查系统是否运行正常")
SUG_C221 = ("1、执行备份："
            "</br>#cp -np /etc/securetty /etc/securetty_bak "
            "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
            "</br>2、禁止root用户远程登录系统："
            "</br>#vi /etc/securetty "
            "</br>注释形如pts/x的行，保存退出，则禁止了root从telnet登录。"
            "</br>#vi /etc/ssh/sshd_config "
            "</br>修改PermitRootLogin设置为no并不被注释，保存退出，则禁止了root从ssh登录。"
            "</br>3、重启sshd服务:"
            "</br>#systemctl restart sshd")
SUG_C222 = ("1、执行备份："
            "</br>#cp -np /etc/passwd /etc/passwd_bak "
            "</br>#cp -np /etc/shadow /etc/shadow_bak "
            "</br>2、锁定无用帐户："
            "</br>方法一："
            "</br>#vi /etc/shadow 在需要锁定的用户名的密码字段前面加!!，如：test:!!$1$QD1ju03H$LbV4vdBbpw.MY0hZ2D/Im1:14805:0:99999:7::: "
            "</br>方法二："
            "</br>#passwd -l test "
            "</br>3、将/etc/passwd文件中的shell域设置成/bin/false。"
            "</br>补充操作说明：lp,uucp,nobody,games,rpm,smmsp,nfsnobody这些帐户不存在或者它们的密码字段为!! "
            "</br>注意：在/etc/shadow文件中若账号的密码段为*号，同时需要在/etc/passwd文件中该账号的shell域（即第6个“：”后面）设置/bin/false才合规。")
SUG_C231_01 = ("1、执行备份："
               "</br>#cp -np /etc/shadow /etc/shadow_bak"
               "userdel username 删除账户已过期的用户")
SUG_C231_02 = ("文件 /etc/shadow 不存在，请检查系统是否运行正常")
SUG_C241 = ("1、执行备份："
           "</br>#cp -mp etc/pam.d/su /etc/pam.d/su_bak "
           "</br>2、修改配置："
           "</br>auth required pam_wheel.so use_uid")
SUG_C251 = ("请确保/etc/passwd文件的权限为644")
SUG_C252 = ("请确保/etc/shadow文件的权限为400")
SUG_C253 = ("请确保/etc/group文件的权限为644")
SUG_C254 = ("请确保/etc/gshadow文件的权限为0")
SUG_C255 = ("请确保/etc/passwd-文件的权限为644")
SUG_C256 = ("请确保/etc/shadow-文件的权限为400")
SUG_C257 = ("请确保/etc/group-文件的权限为644")
SUG_C258 = ("请确保/etc/gshadow-文件的权限为0")
SUG_C259 = ("1、检查/etc/ssh/sshd_config权限配置正确"
           "</br>修改不符合权限配置的密钥文件权限")

SUG_C271 = ("1、执行备份："
            "</br>#cp -np /etc/selinux/config /etc/selinux/config_bak "
            "</br>2、修改selinux设置："
            "</br>SELINUX=permissive")
SUG_C311_01 = ("1、重新设置auditd开机自启动"
           "</br>#systemctl enable auditd"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查auditd状态"
           "</br>#systemctl is-enabled auditd")

SUG_C311_02 = ("1、尝试安装audit"
           "</br>#yum install audit"
           "</br>查看是否正确安装"
           "</br>2、设置audit开机启动"
           "</br>#systemctl enable auditd")

SUG_C312_01 = ("1、重新设置rsyslog开机自启动"
           "</br>#systemctl enable rsyslog"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查rsyslog状态"
           "</br>#systemctl is-enabled rsyslog")

SUG_C312_02 = ("1、尝试安装rsyslog"
           "</br>#yum install rsyslog"
           "</br>查看是否正确安装"
           "</br>2、设置rsyslog开机启动"
           "</br>#systemctl enable rsyslog")

SUG_C320 = ("1、执行备份："
            "</br>#cp -np /etc/audit/rules.d/audit.rules /etc/audit/rules.d/audit.rules_bak "
            "</br>添加正确的audit规则")

SUG_C331 = ("1、执行备份："
            "</br>#cp -np /etc/audit/auditd.conf /etc/audit/auditd.conf_bak "
            "</br>修改其中max_log_file_action=keep_logs")


SUG_C332 = ("1、执行备份："
            "</br>#cp -np /etc/audit/auditd.conf /etc/audit/auditd.conf_bak "
            "</br>修改其中space_left_action=email"
            "</br>修改其中action_mail_acct=root"
            "</br>修改其中admin_space_left_action=halt")
SUG_C411 = ("Remove the ftp software in your Linux System")
SUG_C412 = ("Remove the kexec-tools software in your Linux System")
SUG_C413 = ("Remove the  Ypbind software in your Linux System")
SUG_C415 = ("1、检查当前系统是否安装aide："
           "</br>#rpm -q aide"
           "</br>命令行返回值为空的话手动安装aide"
           "</br>#yum install aide")

SUG_C416 = ("1、检查当前系统是否安装chrony："
           "</br>#rpm -q chrony"
           "</br>命令行返回值为空的话手动安装chrony"
           "</br>#yum install chrony")
SUG_C421 = ("Please disable the nfs-server in your Linux System")
SUG_C422 = ("Please disable the DNS server  in your Linux System")
SUG_C423 = ("1、检查当前dhcp状态："
           "</br>#systemctl disable dhcpd"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查dhcp状态"
           "</br>#systemctl is-enabled dhcpd")

SUG_C424 = ("1、检查当前RPC状态："
           "</br>#systemctl disable rpcbind"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查RPC状态"
           "</br>#systemctl is-enabled rpcbind")

SUG_C425 = ("1、检查当前samba状态："
           "</br>#systemctl disable smb"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查samba状态"
           "</br>#systemctl is-enabled smb")

SUG_C426 = ("1、检查当前SNMP状态："
           "</br>#systemctl disable snmpd"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查SNMP状态"
           "</br>#systemctl is-enabled snmpd")

SUG_C427 = ("1、检查当前IMAP、POP3状态："
           "</br>#systemctl disable dovecot"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查IMAP、POP3状态"
           "</br>#systemctl is-enabled dovecot")

SUG_C428 = ("1、检查当前ntalk状态："
           "</br>#systemctl disable ntalk"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查ntalk状态"
           "</br>#systemctl is-enabled ntalk")

SUG_C429 = ("1、检查当前rsh状态："
           "</br>#systemctl disable rsh.socket"
           "</br>看命令行返回的内容是否执行成功"
           "</br>再次检查rsh状态"
           "</br>#systemctl is-enabled rsh.socket")

SUG_C1021 = ("1、执行备份："
            "</br>#cp -np /etc/profile /etc/profile_bak "
            "</br>修改其中HISTSIZE为大于50小于100的值")
