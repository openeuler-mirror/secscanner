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

WRN_C01 = "No /etc/motd set"

WRN_C02_01 = "No password remember times"
WRN_C02_02 = "Password Remember num is not right"

WRN_C03_01 = "Wrong password minLen set"
WRN_C03_02 = "No password minLen set"
WRN_C03_03 = "Wrong password minclass set"
WRN_C03_04 = "No password minclass set"
WRN_C03_05 = "Wrong Password ucredit set"
WRN_C03_06 = "No password ucredit set"
WRN_C03_07 = "Wrong password lcredit set"
WRN_C03_08 = "No password lcredit set"
WRN_C03_09 = "wrong Password dcredit set"
WRN_C03_10 = "No Password dcredit set"
WRN_C03_11 = "wrong Password ocredit set"
WRN_C03_12 = "No Password ocredit set"

WRN_C04_01 = "wrong user login lock Deny set"
WRN_C04_02 = "No user login lock Deny set"

WRN_C05 = "You should disable ICMP redirect"

WRN_C06 = "Umask value is not 027, need change for secure"

WRN_C07_01 = "No TMOUT set, and this not safe"
WRN_C07_02 = "Wrong TMOUT set, and this not safe"

WRN_C08_1 = "file /etc/passwd's property is not safe"
WRN_C08_2 = "file /etc/gruop's property is not safe"
WRN_C08_3 = "file /etc/grub2.conf's property is not safe"
WRN_C08_4 = "file /boot/grub2/grub.cfg's property is not safe"
WRN_C08_5 = "file /etc/lilo.conf's property is not safe"
WRN_C08_6 = "file  /etc/shadow's property is not safe"
WRN_C08_7 = "dir /etc/security's property is not safe"
WRN_C08_8 = "dir /etc/rc.d/init.d's property is not safe"
WRN_C08_9 = "dir /etc/rc0.d's property is not safe"
WRN_C08_10 = "dir /etc/rc1.d's property is not safe"
WRN_C08_11 = "dir /etc/rc2.d's property is not safe"
WRN_C08_12 = "dir /etc/rc3.d's property is not safe"
WRN_C08_13 = "dir /etc/rc4.d's property is not safe"
WRN_C08_14 = "dir /etc/rc5.d's property is not safe"
WRN_C08_15 = "dir /etc/rc6.d's property is not safe"
WRN_C08_16 = "dir /tmp's property is not safe"

WRN_C09_01 = "PASS_MAX_DAYS value is not safe"
WRN_C09_02 = "PASS_MAX_DAYS value is null"
WRN_C09_03 = "PASS_MIN_DAYS value is not safe"
WRN_C09_04 = "PASS_MIN_DAYS value is null"
WRN_C09_05 = "PASS_MIN_LEN value is not safe"
WRN_C09_06 = "PASS_MIN_LEN value is null"
WRN_C09_07 = "PASS_WARN_AGE value is not safe"
WRN_C09_08 = "PASS_WARN_AGE value is null"

WRN_C10_01 = "No ssh banner config set, need add"
WRN_C10_02 = "The ssh banner is not set, please check the /etc/sshbanner and /etc/ssh/sshd_config"

WRN_C11 = "No ssh algorithms config set, need add"

WRN_C12_01 = "Wrong ssh gssapi setting, need change"
WRN_C12_02 = "No ssh gssapi config set, need add"

WRN_C13_01 = "No ftp restrict directories set, need add"
WRN_C13_02 = "Wrong ftp restrict directories set, need change"

WRN_C14_01 = "No ssh Root Deny setting, need add"
WRN_C14_02 = "Wrong ssh Root Deny setting"

WRN_C15_01 = "Has unused software need to be disabled"
WRN_C15_02 = "Unsupport system"

WRN_C16 = "Has unused user need to be disabled"

WRN_C17 = "The security audit model authpriv.info is not set"

WRN_C18 = "The security audit model kern.warn is not set"

WRN_C19 = "The security audit model *err is not set"

WRN_C20 = "The security audit model auth.none is not set"

WRN_C21 = "The system remain issue file"

WRN_C22_01 = "The system soft core limit is not '0'"
WRN_C22_02 = "The system has no soft core limit set"
WRN_C22_03 = "The system hard core limit is not '0'"
WRN_C22_04 = "The system has no hard core limit set"

WRN_C23 = "There is no pam_wheel set"

WRN_C24 = "There is no customer user"

WRN_C25_01 = "No ssh syslogfacility set, need add"
WRN_C25_02 = "Wrong ssh syslogfacility set, need change"

WRN_C26_01 = "No ls and rm aliases set, need add"
WRN_C26_02 = "Wrong ls and rm aliases set, need change"

WRN_C27 = "One or more log file's property is not 600"

WRN_C28_01 = "No ALWAYS_SET_PATH set, need add"
WRN_C28_02 = "Wrong ALWAYS_SET_PATH set, need change"

WRN_C29_01 = "No ssh loglevel set, need add"
WRN_C29_02 = "Wrong ssh loglevel set, need change"

WRN_C30_01 = "No ftp banner set, need add"
WRN_C30_02 = "Wrong ftp banner set, need change"

WRN_C31_01 = "No prohibit anonymous FTP set, need add"
WRN_C31_02 = "Wrong prohibit anonymous FTP set, need change"

WRN_C32_01 = "No reverse path filtering set, need add"
WRN_C32_02 = "Wrong reverse path filtering set, need change"

WRN_C33_01 = "No ssh PermitEmptyPasswords set, need add"
WRN_C33_02 = "Wrong ssh PermitEmptyPasswords set, need change"

WRN_C34_01 = "No system CtrlAltDel Burst Action set, need add"
WRN_C34_02 = "Wrong system CtrlAltDel Burst Action set, need change"

WRN_C35_01 = "No list of users prohibited from login set, need add"
WRN_C35_02 = "Path /etc/login.user.deny not exists,  need create"

WRN_C36_01 = "No disable magic keys set, need add"
WRN_C36_02 = "Wrong disable magic keys set,  need change"

WRN_C37_01 = "No kernel panic on oops set, need add"
WRN_C37_02 = "Wrong kernel panic on oops set,  need change"

WRN_C38 = "No limit of system resources, need add"

ROOTKIT_R01 = "the system maybe infected"


SUG_C01 = ("1、修改文件/etc/motd的内容，如没有该文件，则创建它，并写入内容。"
           "</br>#touch /etc/motd "
           "</br>#echo 'Authorized users only. All activity may be monitored and reported ' > /etc/motd。"
           "</br>2、可根据实际需要修改该文件的内容。"
           "</br>补充操作说明：/etc/motd文件不为空")
SUG_C02 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak  "
           "</br>2、创建文件/etc/security/opasswd，并设置权限："
           "</br>#touch /etc/security/opasswd "
           "</br>#chown root:root /etc/security/opasswd "
           "</br>#chmod 600 /etc/security/opasswd "
           "</br>3、修改策略设置："
           "</br>#vi /etc/pam.d/system-auth "
           "</br>在password的pam_unix.so模块所在行增加remember=5，保存退出。 "
           "</br>类似如下：password sufficient pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=5 "
           "</br>补充操作说明：/etc/pam.d/system-auth文件中存在 password xxx remember值大于等于5")
SUG_C03_01 = ("1、执行备份："
              "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth"
              "</br>password    requisite     pam_pwquality.so ... minlen=8 ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C03_02 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth"
              "</br>password    requisite     pam_pwquality.so ... minclass=-1 ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C03_03 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth"
              "</br>password    requisite     pam_pwquality.so ... ucredit=-1 ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C03_04 = ("1、执行备份："
              "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth"
              "</br>password    requisite     pam_pwquality.so ... lcredit=-1 ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C03_05 = ("1、执行备份："
              "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth "
              "</br>password    requisite     pam_pwquality.so ... dcredit=-1 ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C03_06 = ("1、执行备份："
              "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/pam.d/system-auth"
              "</br>password    requisite     pam_pwquality.so ... ocredit=-1 ..."
              "</br>password    sufficient    pam_unix.so ...")
SUG_C04 = ("1、执行备份："
           "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
           "</br>#cp -np /etc/pam.d/password-auth /etc/pam.d/password-auth_bak "
           "</br>2、修改策略设置："
           "</br>#vi /etc/pam.d/system-auth"
           "</br>#vi /etc/pam.d/password-auth"
           "</br>增加auth required pam_tally2.so deny=5 onerr=fail unlock_time=300到第二行，保存退出；"
           "</br>补充操作说明：使配置生效需重启服务器。"
           "</br>root帐户不在锁定范围内。"
           "</br>若需锁定root，则再deny后添加even_deny_root"
           "</br>帐户被锁定后，可使用faillog -u <username> -r或pam_tally2 --user <username> --reset解锁。"
           "</br>/etc/pam.d/system-auth和/etc/pam.d/password-auth文件中存在deny的值小于等于5")
SUG_C05 = ("1、备份文件："
           "</br>#cp -np /etc/sysctl.conf /etc/sysctl.conf_bak "
           "</br>2、执行："
           "</br>#vi /etc/sysctl.conf，加上net.ipv4.conf.all.accept_redirects=0 "
           "</br>也可以用以下命令修改net.ipv4.conf.all.accept_redirects的值为0 "
           "</br>sysctl -w net.ipv4.conf.all.accept_redirects=03."
           "</br>使得配置生效：sysctl -p "
           "</br>补充操作说明：可能导致路由错误，无法通信。"
           "</br>/etc/sysctl.conf文件配置了net.ipv4.conf.all.accept_redirects等于0")
SUG_C06 = ("1、执行备份："
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
SUG_C07 = ("1、执行备份："
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
SUG_C08_1 = ("1、修改文件权限："
             "</br>#chmod 0644 /etc/passwd "
             "</br>补充操作说明/etc/passwd权限为644")
SUG_C08_2 = ("1、修改文件权限："
             "</br>#chmod 644 /etc/group "
             "</br>补充操作说明/etc/group权限为644")
SUG_C08_3 = ("1、修改文件权限："
             "</br>#chmod 600 /etc/grub2.conf。"
             "</br>补充操作说明/etc/grub2.conf权限为600")
SUG_C08_4 = ("1、修改文件权限："
             "</br>#chmod 600 /boot/grub2/grub.cfg。"
             "</br>补充操作说明/boot/grub2/grub.cfg权限为600")
SUG_C08_5 = ("1、修改文件权限："
             "</br>#chmod 600 /etc/lilo.conf。"
             "</br>补充操作说明/etc/lilo.conf权限为600")
SUG_C08_6 = ("1、修改文件权限："
             "</br>#chmod 400 /etc/shadow。"
             "</br>补充操作说明/etc/shadow/权限为400")
SUG_C08_7 = ("1、修改文件权限："
             "</br>#chmod 751 /etc/security。"
             "</br>补充操作说明/etc/security/权限为751")
SUG_C08_8 = ("1、修改文件权限："
             "</br>#chmod 750 /etc/rc.d/init.d/。"
             "</br>补充操作说明/etc/rc.d/init.d/权限为750")
SUG_C08_9 = ("1、修改文件权限："
             "</br>#chmod 750 /etc/rc0.d/。"
             "</br>补充操作说明/etc/rc0.d/权限为750")
SUG_C08_10 = ("1、修改文件权限："
              "</br>#chmod 750 /etc/rc1.d/。"
              "</br>补充操作说明/etc/rc1.d/权限为750")
SUG_C08_11 = ("1、修改文件权限："
              "</br>#chmod 750 /etc/rc2.d/。"
              "</br>补充操作说明/etc/rc2.d/权限为750")
SUG_C08_12 = ("1、修改文件权限："
              "</br>#chmod 750 /etc/rc3.d/。"
              "</br>补充操作说明/etc/rc3.d/权限为750")
SUG_C08_13 = ("1、修改文件权限："
              "</br>#chmod 750 /etc/rc4.d/。"
              "</br>补充操作说明/etc/rc4.d/权限为750")
SUG_C08_14 = ("1、修改文件权限："
              "</br>#chmod 750 /etc/rc5.d/。"
              "</br>补充操作说明/etc/rc5.d/权限为750")
SUG_C08_15 = ("1、修改文件权限："
              "</br>#chmod 750 /etc/rc6.d/。"
              "</br>补充操作说明/etc/rc6.d/权限为750")
SUG_C08_16 = ("1、修改文件权限："
              "</br>#chmod 750 /tmp。"
              "</br>补充操作说明/tmp权限为750")
SUG_C09_01 = ("1、执行备份："
              "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/login.defs "
              "</br>配置PASS_MAX_DAYS 90，保存退出。"
              "</br>补充操作说明：/etc/login.defs文件中PASS_MAX_DAYS值不大于90")
SUG_C09_02 = ("1、执行备份："
              "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/login.defs "
              "</br>配置PASS_MIN_DAYS 6，保存退出。"
              "</br>补充操作说明：/etc/login.defs文件中PASS_MIN_DAYS值不小于6")
SUG_C09_03 = ("1、执行备份："
              "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/login.defs "
              "</br>配置PASS_MIN_LEN 8，保存退出。"
              "</br>补充操作说明：/etc/login.defs文件中PASS_MIN_LEN值不小于8")
SUG_C09_04 = ("1、执行备份："
              "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
              "</br>2、修改策略设置："
              "</br>#vi /etc/login.defs "
              "</br>配置PASS_WARN_AGE 30，保存退出。"
              "</br>补充操作说明：/etc/login.defs文件中PASS_WARN_AGE值不小于30")
SUG_C10 = ("1、执行备份："
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
           "</br>2、在/etc/sshbanner文件中填入ssh登录的banner信息。"
           "</br>3、配置/etc/ssh/sshd_config中的banner选项："
           "</br>#Banner /etc/sshbanner。"
           "</br>4、重启sshd服务。")
SUG_C11 = ("1、执行备份："
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
           "</br>2、在/etc/ssh/sshd_config中添加cipher配置: "
           "</br>KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256"
           "</br>Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com"
           "</br>MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com"
           "</br>3、重启sshd服务:"
           "</br>#systemctl restart sshd")
SUG_C12 = ("1、执行备份："
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
           "</br>2、在/etc/ssh/sshd_config中添加 "
           "GSSAPIAuthentication no。"
           "</br>3、重启sshd服务:"
           "</br>#systemctl restart sshd")
SUG_C13 = ("1、执行备份："
           "</br>#cp -np /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf_bak "
           "</br>2、在/etc/vsftpd/vsftpd.conf中将chroot_local_user=修改为YES，并取消注释"
           "</br>3、重启vsftpd服务:"
           "</br>#systemctl restart vsftpd")

SUG_C14 = ("1、执行备份："
           "</br>#cp -np /etc/securetty /etc/securetty_bak "
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
           "</br>2、禁止root用户远程登录系统："
           "</br>#vi /etc/securetty "
           "</br>注释形如pts/x的行，保存退出，则禁止了root从telnet登录。"
           "</br>#vi /etc/ssh/sshd_config "
           "</br>修改PermitRootLogin设置为no并不被注释，保存退出，则禁止了root从ssh登录。"
           "</br>3、重启sshd服务:"
           "</br>#systemctl restart sshd")
SUG_C15 = ("1、停止相关的服务："
           "</br>#systemctl stop <service>")
SUG_C16 = ("1、执行备份："
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
SUG_C17 = ("1、执行备份："
           "</br>#cp -p /etc/syslog.conf /etc/syslog.conf_bak "
           "</br>2、修改配置："
           "</br>#vi /etc/syslog.conf "
           "</br>配置形如：authpriv.*   /var/log/authlog的语句，保存退出 "
           "</br>3、重启rsyslog服务:"
           "</br>#systemctl restart rsyslog "
           "</br>补充操作说明：auth或者authpriv后面的值不是none")
SUG_C18 = ("1、执行备份："
           "</br>#cp -p /etc/syslog.conf /etc/syslog.conf_bak "
           "</br>2、修改配置："
           "</br>#vi /etc/syslog.conf "
           "</br>配置形如：kern.warn  /var/log/kern.log的语句，保存退出 "
           "</br>3、重启rsyslog服务:"
           "</br>#systemctl restart rsyslog "
           "</br>补充操作说明：auth或者authpriv后面的值不是none")
SUG_C19 = ("1、执行备份："
           "</br>#cp -p /etc/syslog.conf /etc/syslog.conf_bak "
           "</br>2、修改配置："
           "</br>#vi /etc/syslog.conf "
           "</br>配置形如：*.err /var/log/error.log的语句，保存退出 "
           "</br>3、重启rsyslog服务:"
           "</br>#systemctl restart rsyslog "
           "</br>补充操作说明：auth或者authpriv后面的值不是none")
SUG_C20 = ("1、执行备份："
           "</br>#cp -np /etc/syslog.conf /etc/syslog.conf_bak "
           "</br>2、修改配置："
           "</br>#vi /etc/syslog.conf "
           "</br>配置形如：auth.none /var/log/auth.log的语句，保存退出 "
           "</br>3、重启rsyslog服务:"
           "</br>#systemctl restart rsyslog "
           "</br>补充操作说明：auth或者authpriv后面的值不是none")
SUG_C21 = ("1、执行备份："
           "</br>#cp -np /etc/issue /etc/issue_bak"
           "</br>#cp -np /etc/issue.net /etc/issue.net_bak"
           "</br>2、删除/etc/issue /etc/issue.net")
SUG_C22_01 = ("1、执行备份："
              "</br>#cp -np /etc/security/limits.conf  /etc/security/limits.conf_bak "
              "</br>2、修改配置"
              "</br>将'*    soft    core  0' 写入/etc/security/limits.conf")
SUG_C22_02 = ("1、执行备份："
              "</br>#cp -np /etc/security/limits.conf  /etc/security/limits.conf_bak "
              "</br>2、修改配置："
              "</br>将'*    hard    core  0' 写入/etc/security/limits.conf。")
SUG_C23 = ("1、执行备份："
           "</br>#cp -mp etc/pam.d/su /etc/pam.d/su_bak "
           "</br>2、修改配置："
           "</br>auth required pam_wheel.so use_uid")
SUG_C24 = "如果没有需要，则删除多余的用户。"
SUG_C25 = ("1、执行备份："
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
           "</br>2、在/etc/ssh/sshd_config中将SyslogFacility AUTH取消注释"
           "</br>3、重启sshd服务:"
           "</br>#systemctl restart sshd")
SUG_C26 = ("1、执行备份："
           "</br>#cp -np /root/.bashrc /root/.bashrc_bak"
           "</br>2、查看是否存在相关配置，若不存在则添加"
           "</br>alias ls='ls -al'"
           "</br>alias rm='rm -i'")
SUG_C27 = "请确保/var/log/下的敏感日志文件的权限为600"
SUG_C28 = ("1、执行备份："
           "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
           "</br>2、修改策略设置："
           "</br>#vim /etc/login.defs "
           "</br>增加ALWAYS_SET_PATH=yes，保存退出。")
SUG_C29 = ("1、执行备份："
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
           "</br>2、在/etc/ssh/sshd_config中将LogLevel修改为VERBOSE，并取消注释"
           "</br>3、重启sshd服务:"
           "</br>#systemctl restart sshd")
SUG_C30 = ("1、执行备份："
           "</br>#cp -np /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf_bak "
           "</br>2、在/etc/vsftpd/vsftpd.conf中将ftpd_bannerr=修改为Authorized users only. All activity may be monitored and "
           "reported.，并取消注释"
           "</br>3、重启vsftpd服务:"
           "</br>#systemctl restart vsftpd")
SUG_C31 = ("1、执行备份："
           "</br>#cp -np /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf_bak "
           "</br>2、在/etc/vsftpd/vsftpd.conf中将anonymous_enable=修改为NO"
           "reported.，并取消注释"
           "</br>3、重启vsftpd服务:"
           "</br>#systemctl restart vsftpd")
SUG_C32 = ("1、执行备份："
           "</br>#cp -np /etc/sysctl.conf /etc/sysctl.conf_bak "
           "</br>2、修改配置"
           "</br>#vi /etc/sysctl.conf"
           "</br>net.ipv4.conf.all.rp_filter=1 "
           "</br>net.ipv4.conf.default.rp_filter=1 "
           "</br>使得配置生效：sysctl -p")
SUG_C33 = ("1、执行备份："
           "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak"
           "</br>2、修改配置"
           "</br>在/etc/ssh/sshd_config中将PermitEmptyPasswords修改为no，并取消注释"
           "</br>3、重启sshd服务:"
           "</br>#systemctl restart sshd")

SUG_C34 = ("1、执行备份："
           "</br>#cp -np /etc/systemd/system/ctrl-alt-del.target /etc/systemd/system/ctrl-alt-del.target_bak"
           "</br>#cp -np /usr/lib/systemd/system/ctrl-alt-del.target /usr/lib/systemd/system/ctrl-alt-del.target_bak"
           "</br>rm -f /etc/systemd/system/ctrl-alt-del.target"
           "</br>rm -f /usr/lib/systemd/system/ctrl-alt-del.target"
           "</br>2、修改配置"
           "</br>#vi /etc/systemd/system.conf"
           "</br>将#CtrlAltDelBurstAction=reboot-force 修改为CtrlAltDelBurstAction=none"
           "</br>3、重启systemd服务:"
           "</br>#systemctl daemon-reexec")

SUG_C35 =("1、执行备份："
          "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak"
          "</br>#cp -np /etc/pam.d/password-auth /etc/pam.d/password-auth_bak"
          "</br>2、创建禁止登陆的用户列表文件"
          "</br>#touch /etc/login.user.deny"
          "</br>3、修改配置"
          "</br>#vi /etc/pam.d/system-auth"
          "</br>#vi /etc/pam.d/password-auth"
          "</br>添加 auth        requisite     pam_listfile.so item=user onerr=succeed sense=deny file=/etc/login.user.deny")

SUG_C36 = ("1、执行备份："
           "</br>#cp -np /etc/sysctl.conf /etc/sysctl.conf_bak "
           "</br>2、修改配置"
           "</br>#vi /etc/sysctl.conf"
           "</br>kernel.sysrq=0 "
           "</br>使得配置生效：sysctl -p"
           "</br>或在/etc/rc.local中增加一行“/sbin/sysctl -p /etc/sysctl.conf")

SUG_C37 = ("1、执行备份："
           "</br>#cp -np /etc/sysctl.conf /etc/sysctl.conf_bak "
           "</br>#cp -np /etc/rc.local /etc/rc.local_bak "
           "</br>#cp -np /lib/systemd/system/rc-local.service /lib/systemd/system/rc-local.service_bak"
           "</br>2、修改配置"
           "</br>#vi /etc/sysctl.conf"
           "</br>kernel.panic_on_oops=1 "
           "</br>#vi /etc/rc.local"
           "</br>/sbin/sysctl -p /etc/sysctl.conf"
           "</br>#vi /lib/systemd/system/rc-local.service"
           "</br>[install]\n"
           "</br>wantedBy=multi-user.target"
           "</br>chmod o+x /etc/rc.local"
           "</br>#vi /etc/rc.local"
           "</br>#!/bin/sh -e\nkernel.panic_on_oops =1\nrm -rf /lib/systemd/system/ctrl-alt-del.target"
           "</br>exit 0 保存退出")

SUG_C38 = ("1、执行备份："
              "</br>#cp -np /etc/security/limits.conf  /etc/security/limits.conf_bak "
              "</br>2、修改配置"
              "</br>soft stack 1024"
              "</br>hard stack 1024"
              "</br>* hard rss 100000"
              "</br>* hard nproc 4000"
              "</br>* hard maxlogins 3 写入/etc/security/limits.conf")

SUG_R01 = "请重新检查问题文件，或删除病毒文件，或重装系统"
