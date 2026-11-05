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
#WARNING
# 初始部署
WRN_C0116_01 = "The symlinks protection is disabled, need change"
WRN_C0116_02 = "The hardlinks protection is disabled, need change"
WRN_C0117 = "The prohibition of usb devices is disabled, need change"
WRN_C0119 = "Wrong set of LD_LIBRARY_PATH in your Linux System"
WRN_C0122_1 = "The FTP software is installed in your Linux System"
WRN_C0122_2 = "The TFTP software is installed in your Linux System"
WRN_C0122_3 = "The Telnet software is installed in your Linux System"
WRN_C0122_4 = "The Net-snmp software is installed in your Linux System"
WRN_C0122_5 = "The Python2 software is installed in your Linux System"
WRN_C0123 = "The debug-shell server is enabled in your Linux System"
WRN_C0124 = "The rsyncd server is enabled in your Linux System"
WRN_C0126 = "The openldap-servers software is installed in your Linux System "
WRN_C0127 = "The cups software is installed in your Linux System "
WRN_C0128 = "The ypserv software is installed in your Linux System "
WRN_C0129 = "The ypbind software is installed in your Linux System "
WRN_C0130 = "The openldap-clients software is installed in your Linux System "
WRN_C0131 = "The network sniffing tool is installed in your Linux System "
WRN_C0134 = "The xorg-x11 software is installed in your Linux System "
WRN_C0135 = "The httpd software is installed in your Linux System "
WRN_C0136 = "The samba software is installed in your Linux System "
WRN_C0137 = "The DNS server is enabled in your Linux System"
WRN_C0138 = "The NFS server is enabled in your Linux System"
WRN_C0139 = "The RPC server is enabled in your Linux System"
WRN_C0140 = "The DHCP server is enabled in your Linux System"

# SUGGESTION
SUG_C0116_01 = ("Please enable the softlink file protection function:"
              "</br>sysctl -w fs.protected_symlinks=1")
SUG_C0116_02 = ("Please enable the hardlink file protection function"
              "</br>sysctl -w fs.protected_hardlinks=1")
SUG_C0117 =   ("Please disable the Usb device: "
              "</br>echo \"install usb-storage /bin/true\" | sudo tee /etc/modprobe.d/prohibit_usb.conf")
SUG_C0119 =   ("Please check the value of LD_LIBRARY_PATH in your Linux System")
SUG_C0122_1 = ("Remove the ftp software in your Linux System")
SUG_C0122_2 = ("Remove the tftp software in your Linux System")
SUG_C0122_3 = ("Remove the telnet software in your Linux System")
SUG_C0122_4 = ("Remove the net-snmp software in your Linux System")
SUG_C0122_5 = ("Remove the python2 software in your Linux System")
SUG_C0123 = ("Disable the debug-shell in your Linux System")
SUG_C0124 = ("Disable the rsyncd in your Linux System")
SUG_C0126 = ("Remove the openldap-servers software in your Linux System")
SUG_C0127 = ("Remove the cups software in your Linux System")
SUG_C0128 = ("Remove the ypserv software in your Linux System")
SUG_C0129 = ("Remove the ypbind software in your Linux System")
SUG_C0130 = ("Remove the openldap-clients software in your Linux System")
SUG_C0131 = ("Remove the network sniffing tool in your Linux System")
SUG_C0134 = ("Remove the xorg-x11 software in your Linux System")
SUG_C0135 = ("Remove the httpd software in your Linux System")
SUG_C0136 = ("Remove the samba software in your Linux System")
SUG_C0137 = ("Disable the DNS in your Linux System")
SUG_C0138 = ("Disable the NFS in your Linux System")
SUG_C0139 = ("Disable the RPC in your Linux System")
SUG_C0140 = ("Disable the DHCP in your Linux System")

# 安全访问
WRN_C0201 = "Has unused user need to be disabled"

WRN_C0204_01 = "There are users with UID 0 who are not root"
WRN_C0204_02 = "Failed to obtain information with UID 0"
WRN_C0204_03 = "file /etc/passwd does not exist"

WRN_C0205_1 = "file /etc/passwd property is not safe"
WRN_C0205_2 = "file /etc/groupp roperty is not safe"
WRN_C0205_3 = "file /etc/passwd- property is not safe"
WRN_C0205_4 = "file /etc/group- property is not safe"
WRN_C0205_5 = "file /etc/shadow property is not safe"
WRN_C0205_6 = "file /etc/gshadow property is not safe"
WRN_C0205_7 = "file /etc/shadow- property is not safe"
WRN_C0205_8 = "file /etc/gshadow- property is not safe"

WRN_C0206_01 = "At least one account does not have a home folder"
WRN_C0206_02 = "At least one home directory does not match the user"
WRN_C0206_03 = "There are issues with the user and their home directory"
WRN_C0206_04 = "Failed to obtain passwd user list"
WRN_C0206_05 = "file /etc/passwd not exists"

WRN_C0207_01 = "Group for user not found"
WRN_C0207_02 = "file /etc/group or /etc/passwd does not exist"

WRN_C0208_01 = "There are duplicate UIDs present"
WRN_C0208_02 = "Failed to retrieve users for UID"
WRN_C0208_03 = "Failed to retrieve UID information"
WRN_C0208_04 = "file /etc/passwd not exists"

WRN_C0209_01 = "Duplicate users found in /etc/passwd"
WRN_C0209_02 = "file /etc/passwd not exists"

WRN_C0210_01 = "There are duplicate GIDs present"
WRN_C0210_02 = "Failed to retrieve GID information"
WRN_C0210_03 = "file /etc/group not exists"

WRN_C0212_01 = "At least one account has expired"
WRN_C0212_02 = "file /etc/shadow dose not exist"

WRN_C0213_01 = "At least one .forward file in the Home directory"
WRN_C0213_02 = "Failed to obtain passwd user's home list"
WRN_C0213_03 = "file /etc/passwd does not exist"

WRN_C0214_01 = "At least one .netrc file in the Home directory"
WRN_C0214_02 = "Failed to obtain passwd user's home list"
WRN_C0214_03 = "file /etc/passwd does not exist"

WRN_C0215_01 = "Wrong password minLen set"
WRN_C0215_02 = "No password minLen set"
WRN_C0215_03 = "Wrong password minclass set"
WRN_C0215_04 = "No password minclass set"
WRN_C0215_05 = "Wrong Password ucredit set"
WRN_C0215_06 = "No password ucredit set"
WRN_C0215_07 = "Wrong password lcredit set"
WRN_C0215_08 = "No password lcredit set"
WRN_C0215_09 = "wrong Password dcredit set"
WRN_C0215_10 = "No Password dcredit set"
WRN_C0215_11 = "wrong Password ocredit set"
WRN_C0215_12 = "No Password ocredit set"
WRN_C0215_13 = "No enforce for root set"

WRN_C0216_01 = "No password remember times"
WRN_C0216_02 = "Password Remember num is not right"

WRN_C0221_01 = "PASS_MAX_DAYS value is not safe"
WRN_C0221_02 = "PASS_MAX_DAYS value is null"
WRN_C0221_03 = "PASS_MIN_DAYS value is not safe"
WRN_C0221_04 = "PASS_MIN_DAYS value is null"
WRN_C0221_05 = "PASS_MIN_LEN value is not safe"
WRN_C0221_06 = "PASS_MIN_LEN value is null"
WRN_C0221_07 = "PASS_WARN_AGE value is not safe"
WRN_C0221_08 = "PASS_WARN_AGE value is null"

WRN_C0222_01 = "There is an empty password user present"
WRN_C0222_02 = "file /etc/shadow not exists"

WRN_C0226_01 = "wrong user login lock Deny set"
WRN_C0226_02 = "No user login lock Deny set"

WRN_C0227_01 = "No TMOUT set, and this not safe"
WRN_C0227_02 = "Wrong TMOUT set, and this not safe"

WRN_C0228_01 = "No /etc/motd warning banner set"
WRN_C0228_02 = "No /etc/issue warning banner set"
WRN_C0228_03 = "No /etc/issue.net warning banner set"

WRN_C0229_01 = "No ssh banner config set, need add"
WRN_C0229_02 = "The ssh banner is not set, please check the /etc/sshbanner and /etc/ssh/sshd_config"

WRN_C0230 = "Wrong HISTSIZE set in /etc/profile"
WRN_C0231 = "Wrong selinux set"

WRN_C0232_01 = "Incorrect SELinux policy settings"
WRN_C0232_02 = "Failed to obtain SELinux policy"

WRN_C0233 = "There is no pam_wheel set"

WRN_C0236_01 = "NO ordinary users cannot use pkexec to configure root privileges set"
WRN_C0236_02 = "file /etc/polkit-1/rules.d/50-default.rules does not exist"

WRN_C0237_01 = "No ALWAYS_SET_PATH set, need add"
WRN_C0237_02 = "Wrong ALWAYS_SET_PATH set, need change"

WRN_C0238_01 = "NO prevent root users from accessing the system locally set"
WRN_C0238_02 = "file /etc/pam.d/system-auth does not exist"

WRN_C0242_01 = "Haveged service inactive"
WRN_C0242_02 = "Failed to obtain the active status of the active state"
WRN_C0242_03 = "Haveged not installed"
WRN_C0242_04 = "Failed to obtain the installation status of haveged"

WRN_C0243_01 = "No global encryption and decryption policy set"
WRN_C0243_02 = "file /etc/crypto-policies/config does not exist"

SUG_C0201 = ("1、执行备份："
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
SUG_C0204_01 = ("1、执行备份："
                "</br>#cp -np /etc/passwd /etc/passwd_bak"
                "</br>#vi /etc/passwd"
                "</br>查看第三位是否存在除root以外为0的用户"
                "</br>若存在，修改该文件或userdel 删除用户")
SUG_C0204_02 = ("1、执行备份："
                "</br>#cp -np /etc/passwd /etc/passwd_bak"
                "</br> awk -F: '($3 == 0) { print $1 }' /etc/passwd 该指令执行失败"
                "</br>手动执行上述指令，查看是否存在报错"
                "</br>若存在则联系技术人员解决")
SUG_C0204_03 = ("文件 /etc/passwd，请检查系统是否运行正常")
SUG_C0205_1 = ("1、修改文件权限："
               "</br>#chmod 0644 /etc/passwd "
               "</br>补充操作说明/etc/passwd权限为644")
SUG_C0205_2 = ("1、修改文件权限："
               "</br>#chmod 644 /etc/group "
               "</br>补充操作说明/etc/group权限为644")
SUG_C0205_3 = ("1、修改文件权限："
               "</br>#chmod 600 /etc/grub2.conf。"
               "</br>补充操作说明/etc/grub2.conf权限为600")
SUG_C0205_4 = ("1、修改文件权限："
               "</br>#chmod 600 /boot/grub2/grub.cfg。"
               "</br>补充操作说明/boot/grub2/grub.cfg权限为600")
SUG_C0205_5 = ("1、修改文件权限："
               "</br>#chmod 600 /etc/lilo.conf。"
               "</br>补充操作说明/etc/lilo.conf权限为600")
SUG_C0205_6 = ("1、修改文件权限："
               "</br>#chmod 400 /etc/shadow。"
               "</br>补充操作说明/etc/shadow/权限为400")
SUG_C0205_7 = ("1、修改文件权限："
               "</br>#chmod 751 /etc/security。"
               "</br>补充操作说明/etc/security/权限为751")
SUG_C0205_8 = ("1、修改文件权限："
               "</br>#chmod 750 /etc/rc.d/init.d/。"
               "</br>补充操作说明/etc/rc.d/init.d/权限为750")
SUG_C0206_01 = ("1、执行备份："
                "</br>#cp -np /etc/passwd /etc/passwd_bak"
                "</br>2、执行下列脚本"
                "</br>#!/bin/bash "
                "</br>grep -E -v '^(halt|sync|shutdown)' \"/etc/passwd\" | awk -F \":\" '($7 != \"/bin/false\" && $7 != \"/sbin/nologin\" && $7 != \"/usr/sbin/nologin\") {print $1 \" \" $6}' | while read name home;"
                "</br>do"
                "</br>  if [ ! -d \"$home\" ]; then"
                "</br>      echo \"No home folder \"$home\" of \"$name\".\""
                "</br>  else"
                "</br>      owner=`ls -l -d $home | awk -F \" \" '{print $3}'`"
                "</br>      if [ \"$owner\" != \"$name\" ]; then"
                "</br>          echo \"\"$home\" is owned by $owner, not \"$name\".\""
                "</br>      fi"
                "</br>  fi"
                "</br>done"
                "</br>执行后，若存在账号没有home目录，则使用先删相应账号"
                "</br>#userdel -r username"
                "</br>需求添加用户账号（自动创建home目录）"
                "</br>#useradd username")
SUG_C0206_02 = ("文件/etc/passwd不存在，请检查系统是否正常运行")
SUG_C0207_01 = ("1、执行备份："
                "</br>#cp -np /etc/passwd /etc/passwd_bak"
                "</br>#cp -np /etc/group /etc/group_bak"
                "</br>2、文件不匹配，有两种修复方法"
                "</br>方法一："
                "</br>通过删除账号，重新添加账号的方式修复："
                "</br>#userdel -r test"
                "</br>#useradd test"
                "</br方法二："
                "</br>通过删除或添加组的方式修复（xxx表示gid的值）"
                "</br>#groupdel testgroup"
                "</br>#groupadd -g xxx testgroup")
SUG_C0207_02 = ("文件/etc/group 或 /etc/passwd不存在，请检查系统是否正常运行")
SUG_C0208_01 = ("1、执行备份："
               "</br>#cp -np /etc/passwd /etc/passwd_bak"
               "</br>将重复UID的用户使用userdel删除")
SUG_C0208_02 = ("该指令 awk -F: '$3 == \"{uid}\" {{ print $1 }}' /etc/passwd 执行失败")
SUG_C0208_03 = ("该指令 cut -f3 -d: /etc/passwd | sort -n | uniq -c 执行失败")
SUG_C0208_04 = ("请检查系统是否存在文件 /etc/passwd")
SUG_C0209_01 = ("分析账号名被重复使用的原因，"
             "</br>手工删除/etc/passwd文件中出现问题的账号，"
             "</br>并按需确定是否使用useradd命令重新添加正确的账号："
             "</br>#useradd test")
SUG_C0209_02 = ("请检查系统是否存在文件 /etc/passwd")
SUG_C0210_01 = ("1、执行备份："
               "</br>#cp -np /etc/group /etc/group"
               "</br>进入文件，将重复GID根据需求删除"
               "</br>保存退出")
SUG_C0210_02 = ("该指令 cut -d: -f3 /etc/group | sort | uniq -d 执行失败")
SUG_C0210_03 = ("请检查系统是否存在文件 /etc/group")
SUG_C0212_01 = ("1、执行备份："
               "</br>#cp -np /etc/shadow /etc/shadow_bak"
               "userdel username 删除账户已过期的用户")
SUG_C0212_02 = ("文件 /etc/shadow 不存在，请检查系统是否运行正常")
SUG_C0213_01 = ("1、执行下列脚本"
                "</br>#!/bin/bash"
                "</br>grep -E -v '^(halt|sync|shutdown)' \"/etc/passwd\" | awk -F \":\" '($7 != \"/bin/false\" && $7 != \"/sbin/nologin\" && $7 != \"/usr/sbin/nologin\") {print $1 \" \" $6}' | while read name home;"
                "</br>do"
                "</br>  if [ -d \"$home\" ]; then"
                "</br>      find $home -name \".forward\""
                "</br>  fi"
                "</br>done"
                "执行后，若存在.forward文件，使用rm命令删除")
SUG_C0213_02 = ("文件/etc/passwd不存在，请检查系统是否正常运行")
SUG_C0214_01 = ("1、执行下列脚本"
                "</br>#!/bin/bash"
                "</br>grep -E -v '^(halt|sync|shutdown)' \"/etc/passwd\" | awk -F \":\" '($7 != \"/bin/false\" && $7 != \"/sbin/nologin\" && $7 != \"/usr/sbin/nologin\") {print $1 \" \" $6}' | while read name home;"
                "</br>do"
                "</br>  if [ -d \"$home\" ]; then"
                "</br>      find $home -name \".netrc\""
                "</br>  fi"
                "</br>done"
                "执行后，若存在.netrc文件，使用rm命令删除")
SUG_C0214_02 = ("文件/etc/passwd不存在，请检查系统是否正常运行")
SUG_C0215_01 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... minlen=8 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0215_02 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... minclass=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0215_03 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... ucredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0215_04 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... lcredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0215_05 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth "
               "</br>password    requisite     pam_pwquality.so ... dcredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0215_06 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... ocredit=-1 ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0215_07 = ("1、执行备份："
               "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/pam.d/system-auth"
               "</br>password    requisite     pam_pwquality.so ... ocredit=-1 enforce_for_root ..."
               "</br>password    sufficient    pam_unix.so ...")
SUG_C0216 = ("1、执行备份：</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak  "
             "</br>2、创建文件/etc/security/opasswd，并设置权限："
             "</br>#touch /etc/security/opasswd "
             "</br>#chown root:root /etc/security/opasswd "
             "</br>#chmod 600 /etc/security/opasswd "
             "</br>3、修改策略设置："
             "</br>#vi /etc/pam.d/system-auth "
             "</br>在password的pam_unix.so模块所在行增加remember=5，保存退出。 "
             "</br>类似如下：password sufficient pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=5 "
             "</br>补充操作说明：/etc/pam.d/system-auth文件中存在 password xxx remember值大于等于5")
SUG_C0221_01 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_MAX_DAYS 90，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_MAX_DAYS值不大于90")
SUG_C0221_02 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_MIN_DAYS 6，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_MIN_DAYS值不小于6")
SUG_C0221_03 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_MIN_LEN 8，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_MIN_LEN值不小于8")
SUG_C0221_04 = ("1、执行备份："
               "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
               "</br>2、修改策略设置："
               "</br>#vi /etc/login.defs "
               "</br>配置PASS_WARN_AGE 30，保存退出。"
               "</br>补充操作说明：/etc/login.defs文件中PASS_WARN_AGE值不小于30")
SUG_C0222_01 = ("1、执行备份："
               "</br>#cp -np /etc/shadow /etc/shadow_bak"
               "</br>执行awk -F: '($2 == \"\") { print $1}' /etc/shadow "
               "</br>若存在输出，则将输出的用户名锁定"
               "</br>使用passwd -l username 锁定用户")
SUG_C0222_02 = ("请检查系统是否存在文件/etc/shadow")
SUG_C0226 = ("1、执行备份："
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

SUG_C0227 = ("1、执行备份："
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
SUG_C0228_01 = ("1、修改文件/etc/motd的内容，如没有该文件，则创建它，并写入内容。"
                "</br>#touch /etc/motd "
                "</br>#echo 'Authorized users only. All activity may be monitored and reported ' > /etc/motd。"
                "</br>2、可根据实际需要修改该文件的内容。"
                "</br>补充操作说明：/etc/motd文件不为空")
SUG_C0228_02 = ("1、修改文件/etc/issue的内容，如没有该文件，则创建它，并写入内容。"
                "</br>#touch /etc/issue "
                "</br>#echo '\\s' > /etc/issue"
                "</br>#echo 'Kernel \\r on an \\m' >> /etc/issue"
                "</br>2、可根据实际需要修改该文件的内容。"
                "</br>补充操作说明：/etc/issue文件不为空")
SUG_C0228_03 = ("1、修改文件/etc/issue.net的内容，如没有该文件，则创建它，并写入内容。"
                "</br>#touch /etc/issue.net "
                "</br>#echo '\\s' > /etc/issue.net"
                "</br>#echo 'Kernel \\r on an \\m' >> /etc/issue.net"
                "</br>2、可根据实际需要修改该文件的内容。"
                "</br>补充操作说明：/etc/issue.net文件不为空")
SUG_C0229 = ("1、执行备份："
             "</br>#cp -np /etc/ssh/sshd_config /etc/ssh/sshd_config_bak "
             "</br>2、在/etc/sshbanner文件中填入ssh登录的banner信息。"
             "</br>Authorized users only. All activity may be monitored and reported"
             "</br>3、配置/etc/ssh/sshd_config中的banner选项："
             "</br>#Banner /etc/sshbanner。"
             "</br>4、重启sshd服务。")
SUG_C0230 = ("1、执行备份："
            "</br>#cp -np /etc/profile /etc/profile_bak "
            "</br>修改其中HISTSIZE为大于50小于100的值")
SUG_C0231 = ("1、执行备份："
            "</br>#cp -np /etc/selinux/config /etc/selinux/config_bak "
            "</br>2、修改selinux设置："
            "</br>SELINUX=permissive")
SUG_C0232_01 = ("1、执行备份："
	     	"</br>#cp -np /etc/selinux/config /etc/selinux/config_bak"
	     	"</br>2、查看target包是否安装"
	     	"</br>#rpm -qa selinux-policy-targeted"
	     	"</br>若未安装，使用yum安装"
	     	"</br>#yum install -y selinux-policy-targeted"
		"</br>3、查看selinux配置文件"
		"</br>配置SELINUXTYPE=targeted"
		"</br>4、根目录下创建.autorelabel文件，用于系统重启后刷新文件标签"
		"</br>#touch /.autorelabel"
		"</br>5、重启操作系统"
		"</br>6、若应用程序运行异常，需要为应用程序配置合理的SELinux策略")
SUG_C0232_02 = ("sestatus | grep 'Loaded policy name' 指令执行失败，请手动执行排查错误。")
SUG_C0233 = ("1、执行备份："
             "</br>#cp -np etc/pam.d/su /etc/pam.d/su_bak "
             "</br>2、修改配置："
             "</br>auth required pam_wheel.so use_uid")
SUG_C0236_01 = ("1、执行备份："
		"</br>#cp -np /etc/polkit-1/rules.d/50-default.rules /etc/polkit-1/rules.d/50-default.rules_bak"
		"</br>2、修改配置："
		"</br>#vim /etc/polkit-1/rules.d/50-default.rules"
		"</br>polkit.addAdminRule(function(action, subject) {"
		"</br>    return [\"unix-user:0\"];"
		"</br>});")
SUG_C0236_02 = ("文件  /etc/polkit-1/rules.d/50-default.rules不存在，请联系技术人员")
SUG_C0237 = ("1、执行备份："
             "</br>#cp -np /etc/login.defs /etc/login.defs_bak "
             "</br>2、修改策略设置："
             "</br>#vim /etc/login.defs "
             "</br>增加ALWAYS_SET_PATH=yes，保存退出。")
SUG_C0238_01 = ("1、执行备份："
                "</br>#cp -np /etc/pam.d/system-auth /etc/pam.d/system-auth_bak"
                "</br>#cp -np /etc/security/access.conf /etc/security/access.conf_bak"
                "</br>添加account类型的pam_access.so模块，且该模块必须在sufficient控制行之前加载"
                "</br>2、修改配置："
                "</br>#vim /etc/pam.d/system-auth"
                "</br>account     required      pam_unix.so"
                "</br>account     required      pam_faillock.so"
                "</br>account     required      pam_access.so"
                "</br>account     sufficient     pam_localuser.so"
                "</br>3、在/etc/security/access.conf文件中添加对root用户登录tty1的限制："
                "</br># vim /etc/security/access.conf"
                "</br>-:root:tty1")
SUG_C0238_02 = ("请检查系统是否存在文件etc/pam.d/system-auth")
SUG_C0242_01 = ("开启haveged服务："
		"</br># systemctl start haveged"
		"</br>如果要将其设置为随系统启动，可以这样配置："
		"</br># systemctl enable haveged.service")
SUG_C0242_02 = ("查看是否已安装启haveged"
		"</br># rpm -qa haveged"
		"</br>若未安装"
		"</br># yum install -y haveged"
		"</br>安装后查看服务状态"
		"</br># systemctl is-active haveged"
		"</br>如果显示处于active状态，说明haveged服务正在运行，反之如果显示处于inactive状态，说明服务未开启。"
		"</br>若未开启使用systemctl start haveged开启服务"
		"</br>如果要将其设置为随系统启动:systemctl enable haveged.service")
SUG_C0243_01 = ("1、执行备份："
		"</br>#cp -np /etc/crypto-policies/config /etc/crypto-policies/config_bak"
		"</br>2、修改策略设置："
		"</br># vim /etc/crypto-policies/config"
		"</br>DEFAULT")
SUG_C0243_02 = ("请检查系统是否存在文件/etc/crypto-policies/config")

WRN_C0301_01 = "Found sctp and tipc should be avoided"
WRN_C0301_02 = "Found tipc should be avoided"
WRN_C0301_03 = "Found sctp should be avoided"
WRN_C0302 = "Wireless network should be banned"
WRN_C0303_01 = "Found Firewalld is active, iptables or nftables actice too"
WRN_C0303_02 = "Found Firewalld is inactive(dead)"
WRN_C0320 = "Found wrong set of ssh authentication"
WRN_C0322_01 = "Wrong set of PubkeyAcceptedKeyTypes"
WRN_C0322_02 = "Wrong set of PubkeyAcceptedKeyTypes"
WRN_C0323 = "Wrong set of PAM in sshd config file"
WRN_C0330 = "Wrong set of maxstartups in sshd config file"
WRN_C0331 = "Wrong set of MaxSessions in sshd config file"
WRN_C0332 = "Wrong set of X11forwarding in sshd config file"
WRN_C0333 = "Wrong set of MaxAuthTries in sshd config file"
WRN_C0334 = "Wrong set of PermitUserEnvironment in sshd config file"
WRN_C0335 = "Wrong set of LoginGraceTime in sshd config file"
WRN_C0336 = "Found ssh authorized_keys in /home/ /root/"
WRN_C0337 = "Found ssh known_hosts in /home/ /root/"
WRN_C0338_01 = "Found deprecated option of sshd"
WRN_C0338_02 = "Error occured while excute sshd -t command"
WRN_C0339 = "Wrong set of AllowTcpForwarding in sshd config file"
WRN_C0345 = "Wrong set of kernel.dmesg_restrict in sysctl config file"
WRN_C0346 = "Wrong set of kernel.kptr_restrict in sysctl config file"
WRN_C0349 = "Wrong set of ignore ICMP broadcast in sysctl config file"
WRN_C0350 = "Wrong set of ban accept ICMP redirect in sysctl config file"
WRN_C0351 = "Wrong set of ban send ICMP redirect in sysctl config file"
WRN_C0364 = "Wrong set of kernel.sysrq in sysctl config file"
WRN_C0365 = "Wrong set of kernel.yama.ptrace_scope in sysctl config file"

SUG_C0301_01 = ("避免使用不常见网络服务")
SUG_C0301_02 = ("避免使用不常见网络服务")
SUG_C0301_03 = ("避免使用不常见网络服务")
SUG_C0302 = ("避免使用无线网络")
SUG_C0303_01 = ("应当启用firewalld服务")
SUG_C0303_02 = ("应当启用firewalld服务")
SUG_C0320 = ("确保SSH服务认证方式配置正确")
SUG_C0322_01 = ("确保用户认证密钥算法配置正确")
SUG_C0322_02 = ("确保用户认证密钥算法配置正确")
SUG_C0323 = ("确保PAM认证使能")
SUG_C0330 = ("应当正确配置SSH并发未认证连接数")
SUG_C0331 = ("应当正确配置单个SSH连接允许的并发会话数")
SUG_C0332 = ("禁止使用X11 Forwarding")
SUG_C0333 = ("应当正确配置MaxAuthTries")
SUG_C0334 = ("禁止使用PermitUserEnvironment")
SUG_C0335 = ("应当正确配置LoginGraceTime")
SUG_C0336 = ("禁止SSH服务预设置authorized_keys")
SUG_C0337 = ("禁止SSH服务预设置known_hosts")
SUG_C0338_01 = ("禁止SSH服务配置弃用的选项")
SUG_C0338_02 = ("禁止SSH服务配置弃用的选项")
SUG_C0339 = ("确保禁用SSH的TCP转发功能")
SUG_C0345 = ("确保dmesg访问权限配置正确")
SUG_C0346 = ("确保正确配置内核参数kptr_restrict")
SUG_C0364 = ("确保正确配置内核参数sysrq")
SUG_C0365 = ("确保正确配置内核参数yama.ptrace_scope")
# 1 初始部署 - 文件系统
WRN_C01101_01 = "There are files or directories without owner in your Linux System, need change"
WRN_C01101_02 = "There are files or directories without group in your Linux System, need change"
WRN_C01102 = "There are null link files in your Linux System, need change"
WRN_C01103 = "There are hidden executable files in your Linux System, need change"
WRN_C01104 = "There are world writable directories without sticky bit set, need change"
WRN_C01105 = "Wrong set of UMASK in your Linux System, need change"
WRN_C01106 = "There are world writable files in your Linux System, need change"
WRN_C01107_01 = "The cramfs filesystem is not banned from being mounted, need change"
WRN_C01107_02 = "The freevxfs filesystem is not banned from being mounted, need change"
WRN_C01107_03 = "The jffs2 filesystem is not banned from being mounted, need change"
WRN_C01107_04 = "The hfs filesystem is not banned from being mounted, need change"
WRN_C01107_05 = "The hfsplus filesystem is not banned from being mounted, need change"
WRN_C01107_06 = "The squashfs filesystem is not banned from being mounted, need change"
WRN_C01107_07 = "The udf filesystem is not banned from being mounted, need change"
WRN_C01107_08 = "The vfat filesystem is not banned from being mounted, need change"
WRN_C01107_09 = "The fat filesystem is not banned from being mounted, need change"
WRN_C01107_10 = "The msdos filesystem is not banned from being mounted, need change"
WRN_C01107_11 = "The nfs filesystem is not banned from being mounted, need change"
WRN_C01107_12 = "The ceph filesystem is not banned from being mounted, need change"
WRN_C01107_13 = "The fuse filesystem is not banned from being mounted, need change"
WRN_C01107_14 = "The overlay filesystem is not banned from being mounted, need change"
WRN_C01107_15 = "The xfs filesystem is not banned from being mounted, need change"
WRN_C01108 = "There are partitions not mounted with ro option, need change"
WRN_C01109 = "There are partitions not mounted with nodev option, need change"
WRN_C01110 = "There are partitions not mounted with noexec option, need change"
WRN_C01111 = "There are removable device partitions not mounted with nodev and noexec options, need change"
WRN_C01112 = "There are partitions not mounted with nosuid option, need change"
WRN_C01113 = "There are files with unnecessary SUID or SGID bits set, need change"
WRN_C01114_01 = "The permission of /etc/passwd is not safe, need change"
WRN_C01114_02 = "The permission of /etc/group is not safe, need change"
WRN_C01114_03 = "The permission of /etc/shadow is not safe, need change"
WRN_C01114_04 = "The permission of /etc/gshadow is not safe, need change"
WRN_C01114_05 = "The permission of /etc/passwd- is not safe, need change"
WRN_C01114_06 = "The permission of /etc/group- is not safe, need change"
WRN_C01114_07 = "The permission of /etc/shadow- is not safe, need change"
WRN_C01114_08 = "The permission of /etc/gshadow- is not safe, need change"
WRN_C01114_09 = "The permission of /etc/ssh/sshd_config is not safe, need change"
WRN_C01115_01 = "The open file limits of the session are not set correctly, need change"
WRN_C01115_02 = "Wrong set of nofile limits in /etc/security/limits.conf, need change"

SUG_C01101_01 = ("Please confirm these files or directories are useless and delete them, or change the owner to an existing user:"
              "</br>rm test -rf or chown test1:test1 test")
SUG_C01101_02 = ("Please confirm these files or directories are useless and delete them, or change the group to an existing group:"
              "</br>rm test -rf or chown test1:test1 test")
SUG_C01102 = ("Please delete the null link files:"
              "</br>rm ./testlink")
SUG_C01103 = ("Please delete the hidden executable file or remove its executable permission:"
              "</br>rm .testfile or chmod 644 .testfile")
SUG_C01104 = ("Please set the sticky bit on the world writable directories:"
              "</br>chmod 1777 test")
SUG_C01105 = ("Please set the UMASK correctly in /etc/bashrc:"
              "</br>umask 0077")
SUG_C01106 = ("Please remove the world writable permission of the files:"
              "</br>chmod o-w test")
SUG_C01107_01 = ("Please ban the cramfs filesystem from being mounted:"
              "</br>echo \"install cramfs /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_02 = ("Please ban the freevxfs filesystem from being mounted:"
              "</br>echo \"install freevxfs /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_03 = ("Please ban the jffs2 filesystem from being mounted:"
              "</br>echo \"install jffs2 /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_04 = ("Please ban the hfs filesystem from being mounted:"
              "</br>echo \"install hfs /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_05 = ("Please ban the hfsplus filesystem from being mounted:"
              "</br>echo \"install hfsplus /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_06 = ("Please ban the squashfs filesystem from being mounted:"
              "</br>echo \"install squashfs /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_07 = ("Please ban the udf filesystem from being mounted:"
              "</br>echo \"install udf /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_08 = ("Please ban the vfat filesystem from being mounted:"
              "</br>echo \"install vfat /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_09 = ("Please ban the fat filesystem from being mounted:"
              "</br>echo \"install fat /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_10 = ("Please ban the msdos filesystem from being mounted:"
              "</br>echo \"install msdos /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_11 = ("Please ban the nfs filesystem from being mounted:"
              "</br>echo \"install nfs /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_12 = ("Please ban the ceph filesystem from being mounted:"
              "</br>echo \"install ceph /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_13 = ("Please ban the fuse filesystem from being mounted:"
              "</br>echo \"install fuse /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_14 = ("Please ban the overlay filesystem from being mounted:"
              "</br>echo \"install overlay /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01107_15 = ("Please ban the xfs filesystem from being mounted:"
              "</br>echo \"install xfs /bin/true\" >> /etc/modprobe.d/secscanner.conf")
SUG_C01108 = ("Please remount the partitions with the ro option:"
              "</br>mount -o remount,ro <mountpoint>")
SUG_C01109 = ("Please remount the partitions with the nodev option:"
              "</br>mount -o remount,nodev <mountpoint>")
SUG_C01110 = ("Please remount the partitions with the noexec option:"
              "</br>mount -o remount,noexec <mountpoint>")
SUG_C01111 = ("Please remount the removable device partitions with the nodev and noexec options:"
              "</br>mount -o remount,nodev,noexec <mountpoint>")
SUG_C01112 = ("Please remount the partitions with the nosuid option:"
              "</br>mount -o remount,nosuid <mountpoint>")
SUG_C01113 = ("Please review the files and remove the unnecessary SUID and SGID bits:"
              "</br>chmod u-s,g-s <file>")
SUG_C01114_01 = ("Please change the permission of /etc/passwd to 0644:"
              "</br>chmod 0644 /etc/passwd")
SUG_C01114_02 = ("Please change the permission of /etc/group to 0644:"
              "</br>chmod 0644 /etc/group")
SUG_C01114_03 = ("Please change the permission of /etc/shadow to 0000:"
              "</br>chmod 0000 /etc/shadow")
SUG_C01114_04 = ("Please change the permission of /etc/gshadow to 0000:"
              "</br>chmod 0000 /etc/gshadow")
SUG_C01114_05 = ("Please change the permission of /etc/passwd- to 0644:"
              "</br>chmod 0644 /etc/passwd-")
SUG_C01114_06 = ("Please change the permission of /etc/group- to 0644:"
              "</br>chmod 0644 /etc/group-")
SUG_C01114_07 = ("Please change the permission of /etc/shadow- to 0000:"
              "</br>chmod 0000 /etc/shadow-")
SUG_C01114_08 = ("Please change the permission of /etc/gshadow- to 0000:"
              "</br>chmod 0000 /etc/gshadow-")
SUG_C01114_09 = ("Please change the permission of /etc/ssh/sshd_config to 0600:"
              "</br>chmod 0600 /etc/ssh/sshd_config")
SUG_C01115_01 = ("Please set the open file limits correctly:"
              "</br>ulimit -n 3000")
SUG_C01115_02 = ("Please set the nofile limits correctly in /etc/security/limits.conf:"
              "</br>* soft nofile 2000"
              "</br>* hard nofile 10000")

# 1 初始部署 - 软件
WRN_C01206 = "Some repo configuration files in /etc/yum.repos.d do not set gpgcheck=1 or lack the GPG public key configuration"
WRN_C01209 = "The avahi software is installed in your Linux System"
WRN_C01215_01 = "The wireshark software is installed in your Linux System"
WRN_C01215_02 = "The netcat software is installed in your Linux System"
WRN_C01215_03 = "The tcpdump software is installed in your Linux System"
WRN_C01215_04 = "The nmap software is installed in your Linux System"
WRN_C01215_05 = "The ethereal software is installed in your Linux System"
WRN_C01216_01 = "The strace software is installed in your Linux System"
WRN_C01216_02 = "The gdb software is installed in your Linux System"
WRN_C01216_03 = "The perf software is installed in your Linux System"
WRN_C01216_04 = "The binutils-extra software is installed in your Linux System"
WRN_C01216_05 = "The appict software is installed in your Linux System"
WRN_C01216_06 = "The kmem_analyzer_tools software is installed in your Linux System"
WRN_C01217_01 = "The gcc software is installed in your Linux System"
WRN_C01217_02 = "The cpp software is installed in your Linux System"
WRN_C01217_03 = "The mcpp software is installed in your Linux System"
WRN_C01217_04 = "The flex software is installed in your Linux System"
WRN_C01217_05 = "The cmake software is installed in your Linux System"
WRN_C01217_06 = "The make software is installed in your Linux System"
WRN_C01217_07 = "The rpm-build software is installed in your Linux System"
WRN_C01217_08 = "The binutils-extra software is installed in your Linux System"
WRN_C01217_09 = "The elfutils-extra software is installed in your Linux System"
WRN_C01217_10 = "The llvm software is installed in your Linux System"
WRN_C01217_11 = "The rpcgen software is installed in your Linux System"
WRN_C01217_12 = "The gcc-c++ software is installed in your Linux System"
WRN_C01217_13 = "The libtool software is installed in your Linux System"

SUG_C01206 = ("Please add gpgcheck=1 and the correct gpgkey to every repo configuration file in /etc/yum.repos.d, or import the GPG public key manually:"
              "</br>rpm --import ./key")
SUG_C01209 = ("Please remove the avahi software in your Linux System:"
              "</br>yum remove avahi"
              "</br>dnf remove avahi")
SUG_C01215_01 = ("Please remove the wireshark software in your Linux System:"
              "</br>rpm -e wireshark")
SUG_C01215_02 = ("Please remove the netcat software in your Linux System:"
              "</br>rpm -e netcat")
SUG_C01215_03 = ("Please remove the tcpdump software in your Linux System:"
              "</br>rpm -e tcpdump")
SUG_C01215_04 = ("Please remove the nmap software in your Linux System:"
              "</br>rpm -e nmap")
SUG_C01215_05 = ("Please remove the ethereal software in your Linux System:"
              "</br>rpm -e ethereal")
SUG_C01216_01 = ("Please remove the strace software in your Linux System:"
              "</br>rpm -e strace")
SUG_C01216_02 = ("Please remove the gdb software in your Linux System:"
              "</br>rpm -e gdb")
SUG_C01216_03 = ("Please remove the perf software in your Linux System:"
              "</br>rpm -e perf")
SUG_C01216_04 = ("Please remove the binutils-extra software in your Linux System:"
              "</br>rpm -e binutils-extra")
SUG_C01216_05 = ("Please remove the appict software in your Linux System:"
              "</br>rpm -e appict")
SUG_C01216_06 = ("Please remove the kmem_analyzer_tools software in your Linux System:"
              "</br>rpm -e kmem_analyzer_tools")
SUG_C01217_01 = ("Please remove the gcc software in your Linux System:"
              "</br>rpm -e gcc")
SUG_C01217_02 = ("Please remove the cpp software in your Linux System:"
              "</br>rpm -e cpp")
SUG_C01217_03 = ("Please remove the mcpp software in your Linux System:"
              "</br>rpm -e mcpp")
SUG_C01217_04 = ("Please remove the flex software in your Linux System:"
              "</br>rpm -e flex")
SUG_C01217_05 = ("Please remove the cmake software in your Linux System:"
              "</br>rpm -e cmake")
SUG_C01217_06 = ("Please remove the make software in your Linux System:"
              "</br>rpm -e make")
SUG_C01217_07 = ("Please remove the rpm-build software in your Linux System:"
              "</br>rpm -e rpm-build")
SUG_C01217_08 = ("Please remove the binutils-extra software in your Linux System:"
              "</br>rpm -e binutils-extra")
SUG_C01217_09 = ("Please remove the elfutils-extra software in your Linux System:"
              "</br>rpm -e elfutils-extra")
SUG_C01217_10 = ("Please remove the llvm software in your Linux System:"
              "</br>rpm -e llvm")
SUG_C01217_11 = ("Please remove the rpcgen software in your Linux System:"
              "</br>rpm -e rpcgen")
SUG_C01217_12 = ("Please remove the gcc-c++ software in your Linux System:"
              "</br>rpm -e gcc-c++")
SUG_C01217_13 = ("Please remove the libtool software in your Linux System:"
              "</br>rpm -e libtool")

# 2 账号与认证
WRN_C02103_01 = "Different accounts share the same initial group ID in /etc/passwd"
WRN_C02103_02 = "USERGROUPS_ENAB is not set to yes in /etc/login.defs"
WRN_C02111 = "Duplicate group names found in /etc/group"
WRN_C02203 = "pam_unix is not enabled in the PAM password stack, users can change their own password without verifying the old password"
WRN_C02204_01 = "pam_pwquality is not enabled in /etc/pam.d/system-auth, the check that the password does not contain the account string cannot take effect"
WRN_C02204_02 = "usercheck=0 is set for pam_pwquality in /etc/pam.d/system-auth, the password is allowed to contain the account name string"
WRN_C02204_03 = "pam_pwquality is not enabled in /etc/pam.d/password-auth, the check that the password does not contain the account string cannot take effect"
WRN_C02204_04 = "usercheck=0 is set for pam_pwquality in /etc/pam.d/password-auth, the password is allowed to contain the account name string"
WRN_C02205_01 = "pam_unix does not use sha512 in /etc/pam.d/system-auth, the password may be encrypted with a weak hash algorithm"
WRN_C02205_02 = "ENCRYPT_METHOD is not set to SHA512 in /etc/login.defs, the password may be encrypted with a weak hash algorithm"
WRN_C02205_03 = "crypt_style is not set to sha512 in /etc/libuser.conf, the password may be encrypted with a weak hash algorithm"
WRN_C02206_01 = "pam_pwquality is not enabled in /etc/pam.d/system-auth, the weak password dictionary check cannot take effect"
WRN_C02206_02 = "dictcheck=0 is set for pam_pwquality in /etc/pam.d/system-auth, the weak password dictionary check is disabled"
WRN_C02206_03 = "dictcheck=0 is set in /etc/security/pwquality.conf, the weak password dictionary check is disabled"
WRN_C02206_04 = "the cracklib weak password dictionary does not exist in /usr/share/cracklib, the weak password dictionary check cannot take effect"
WRN_C02209_01 = "password_pbkdf2 is not configured in grub.cfg, the grub menu can be edited without password verification"
WRN_C02209_02 = "GRUB2_PASSWORD with a pbkdf2 hash is not set in user.cfg, grub password protection is incomplete"
WRN_C02210_01 = "ExecStart in /usr/lib/systemd/system/rescue.service does not use systemd-sulogin-shell, single user mode can be entered without verifying the root password"
WRN_C02210_02 = "ExecStart in /usr/lib/systemd/system/emergency.service does not use systemd-sulogin-shell, single user mode can be entered without verifying the root password"
WRN_C02211_01 = "the password of some normal users is not set to expired, these users will not be forced to change the password at first login"
WRN_C02304_01 = "Banner is not configured in /etc/ssh/sshd_config, no warning banner is shown before ssh login"
WRN_C02304_02 = "the file pointed by the Banner item in /etc/ssh/sshd_config does not exist, the warning banner cannot be shown before ssh login"
WRN_C02405_01 = "sudo is not installed, normal users cannot run privileged programs through sudo"
WRN_C02405_02 = "no (root) sudo rule is configured in /etc/sudoers, normal users cannot run privileged programs as root through sudo"
WRN_C02405_03 = "the wheel group sudo rule is not enabled in /etc/sudoers, users in the wheel group cannot run privileged programs through sudo"
WRN_C02406_01 = "some scripts configured in /etc/sudoers are writable by low privilege users, which can be modified to escalate privileges"
WRN_C02408_01 = "ALWAYS_SET_PATH is not configured in /etc/login.defs, su command may inherit the user PATH environment variable and lead to privilege escalation"
WRN_C02408_02 = "ALWAYS_SET_PATH is not set to yes in /etc/login.defs, su command may inherit the user PATH environment variable and lead to privilege escalation"

SUG_C02103_01 = ("Do not use the -g option when creating a new account so that the system assigns a unique private group automatically, and use the -G option to join other groups:"
              "</br>useradd test"
              "</br>usermod -a -G root test1")
SUG_C02103_02 = ("Please set USERGROUPS_ENAB to yes in /etc/login.defs to ensure each new account is assigned its own group:"
              "</br>USERGROUPS_ENAB yes")
SUG_C02111 = ("Please analyze the reason for the duplicate group names, then remove the duplicate group entries from /etc/group manually and recreate the correct group if needed:"
              "</br>groupadd test")
SUG_C02203 = ("Please enable pam_unix.so in the password stack of /etc/pam.d/system-auth, which verifies the old password by default:"
              "</br>password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok")
SUG_C02204_01 = ("Please enable pam_pwquality.so in the password stack of /etc/pam.d/system-auth and keep usercheck enabled:"
              "</br>password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root try_first_pass local_users_only retry=3 dcredit=0 ucredit=0 lcredit=0 ocredit=0")
SUG_C02204_02 = ("Please remove the usercheck=0 field from the pam_pwquality line in /etc/pam.d/system-auth:"
              "</br>vim /etc/pam.d/system-auth")
SUG_C02204_03 = ("Please enable pam_pwquality.so in the password stack of /etc/pam.d/password-auth and keep usercheck enabled:"
              "</br>password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root try_first_pass local_users_only retry=3 dcredit=0 ucredit=0 lcredit=0 ocredit=0")
SUG_C02204_04 = ("Please remove the usercheck=0 field from the pam_pwquality line in /etc/pam.d/password-auth:"
              "</br>vim /etc/pam.d/password-auth")
SUG_C02205_01 = ("Please add sha512 to the pam_unix line in /etc/pam.d/system-auth:"
              "</br>password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok")
SUG_C02205_02 = ("Please set ENCRYPT_METHOD to SHA512 in /etc/login.defs:"
              "</br>ENCRYPT_METHOD SHA512")
SUG_C02205_03 = ("Please set crypt_style to sha512 in /etc/libuser.conf:"
              "</br>crypt_style = sha512")
SUG_C02206_01 = ("Please enable pam_pwquality.so in the password stack of /etc/pam.d/system-auth:"
              "</br>password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3")
SUG_C02206_02 = ("Please remove the dictcheck=0 field from the pam_pwquality line in /etc/pam.d/system-auth:"
              "</br>vim /etc/pam.d/system-auth")
SUG_C02206_03 = ("Please remove or modify the dictcheck=0 line in /etc/security/pwquality.conf:"
              "</br>vim /etc/security/pwquality.conf")
SUG_C02206_04 = ("Please install the cracklib dictionary package:"
              "</br>dnf install cracklib-dicts")
SUG_C02209_01 = ("Please generate the grub password hash and add the password_pbkdf2 line to grub.cfg:"
              "</br>grub2-mkpasswd-pbkdf2"
              "</br>echo \"GRUB2_PASSWORD=grub.pbkdf2.sha512.10000.xxxx\" > /boot/grub2/user.cfg")
SUG_C02209_02 = ("Please generate the grub password hash and write it into user.cfg:"
              "</br>grub2-mkpasswd-pbkdf2"
              "</br>echo \"GRUB2_PASSWORD=grub.pbkdf2.sha512.10000.xxxx\" > /boot/grub2/user.cfg")
SUG_C02210_01 = ("Please modify the ExecStart item in /usr/lib/systemd/system/rescue.service:"
              "</br>ExecStart=-/usr/lib/systemd/systemd-sulogin-shell rescue")
SUG_C02210_02 = ("Please modify the ExecStart item in /usr/lib/systemd/system/emergency.service:"
              "</br>ExecStart=-/usr/lib/systemd/systemd-sulogin-shell emergency")
SUG_C02211_01 = ("Please expire the password of the user immediately after resetting it:"
              "</br>passwd -e <username>")
SUG_C02304_01 = ("Please configure the Banner item in /etc/ssh/sshd_config and restart the sshd service:"
              "</br>Banner /etc/issue.net"
              "</br>systemctl restart sshd")
SUG_C02304_02 = ("Please create the banner file or modify the Banner item to an existing file:"
              "</br>Banner /etc/issue.net")
SUG_C02405_01 = ("Please install the sudo package:"
              "</br>dnf install sudo")
SUG_C02405_02 = ("Please add a sudo rule for the user or the wheel group in /etc/sudoers:"
              "</br>test_sudo  ALL=(root)  /bin/ping")
SUG_C02405_03 = ("Please enable the wheel group rule in /etc/sudoers:"
              "</br>%wheel  ALL=(ALL)  ALL")
SUG_C02406_01 = ("Please remove the write permission of the low privilege users from the scripts:"
              "</br>chmod a-w <script>")
SUG_C02408 = ("Please add or modify the ALWAYS_SET_PATH item in /etc/login.defs:"
              "</br>ALWAYS_SET_PATH=yes")

# 3 网络 - SSH
WRN_C03301 = "Wrong set of ssh protocol version in sshd config file"
WRN_C03303 = "Wrong set of KexAlgorithms in sshd config file"
WRN_C03306 = "Wrong set of MACs in sshd config file"
WRN_C03307 = "Wrong set of Ciphers in sshd config file"
WRN_C03308 = "Found crypto policy override of sshd"
WRN_C03309 = "Wrong set of PermitRootLogin in sshd config file"

SUG_C03301 = ("Please set the Protocol field to 2 in /etc/ssh/sshd_config and restart the sshd service:"
              "</br>Protocol 2"
              "</br>systemctl restart sshd")
SUG_C03303 = ("Please set the safe SSH key exchange algorithms in /etc/ssh/sshd_config and restart the sshd service:"
              "</br>KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256"
              "</br>systemctl restart sshd")
SUG_C03306 = ("Please set the safe SSH MAC algorithms in /etc/ssh/sshd_config and restart the sshd service:"
              "</br>MACs hmac-sha2-512,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-256-etm@openssh.com"
              "</br>systemctl restart sshd")
SUG_C03307 = ("Please set the safe SSH ciphers in /etc/ssh/sshd_config and restart the sshd service:"
              "</br>Ciphers aes128-ctr,aes192-ctr,aes256-ctr,chacha20-poly1305@openssh.com,aes128-gcm@openssh.com,aes256-gcm@openssh.com"
              "</br>systemctl restart sshd")
SUG_C03308 = ("Please delete or comment out the CRYPTO_POLICY field in /etc/sysconfig/sshd and reload the sshd config:"
              "</br>vim /etc/sysconfig/sshd"
              "</br>systemctl reload sshd")
SUG_C03309 = ("Please set PermitRootLogin to no in /etc/ssh/sshd_config and restart the sshd service:"
              "</br>PermitRootLogin no"
              "</br>systemctl restart sshd")

# 3 网络 - 定时任务与内核参数
WRN_C03401 = "Some scripts in /etc/crontab are writable by group or other users, need change"
WRN_C03402 = "The cron daemon (crond) is not enabled in your Linux System"
WRN_C03403_01 = "The cron daemon (crond) is not enabled in your Linux System"
WRN_C03403_02 = "The owner or permission of /etc/crontab and the cron directories is not safe"
WRN_C03403_03 = "The /etc/cron.deny or /etc/at.deny file exists, which is not safe"
WRN_C03403_04 = "The /etc/cron.allow or /etc/at.allow file does not exist or its permission is not 600"
WRN_C03501 = "The kernel ASLR (randomize_va_space) is not set to 2, need change"
WRN_C03504 = "The kernel SMAP is disabled by the nosmap boot option, need change"
WRN_C03505 = "The kernel SMEP is disabled by the nosmep boot option, need change"
WRN_C03506 = "The system is allowed to respond to ICMP broadcast requests, need change"
WRN_C03507_01 = "The parameter net.ipv4.conf.all.accept_redirects is not set to 0, need change"
WRN_C03507_02 = "The parameter net.ipv6.conf.all.accept_redirects is not set to 0, need change"
WRN_C03507_03 = "The parameter net.ipv4.conf.all.secure_redirects is not set to 0, need change"
WRN_C03507_04 = "The parameter net.ipv4.conf.default.secure_redirects is not set to 0, need change"
WRN_C03508_01 = "The parameter net.ipv4.conf.all.send_redirects is not set to 0, need change"
WRN_C03508_02 = "The parameter net.ipv4.conf.default.send_redirects is not set to 0, need change"
WRN_C03510 = "The system does not ignore bogus ICMP error responses, need change"
WRN_C03511_01 = "The parameter net.ipv4.conf.all.rp_filter is not set to 1, need change"
WRN_C03511_02 = "The parameter net.ipv4.conf.default.rp_filter is not set to 1, need change"
WRN_C03512_01 = "The parameter net.ipv4.ip_forward is not set to 0, need change"
WRN_C03512_02 = "The parameter net.ipv6.conf.all.forwarding is not set to 0, need change"
WRN_C03513_01 = "The parameter net.ipv4.conf.all.accept_source_route is not set to 0, need change"
WRN_C03513_02 = "The parameter net.ipv4.conf.default.accept_source_route is not set to 0, need change"
WRN_C03513_03 = "The parameter net.ipv6.conf.all.accept_source_route is not set to 0, need change"
WRN_C03513_04 = "The parameter net.ipv6.conf.default.accept_source_route is not set to 0, need change"
WRN_C03514 = "The TCP SYN cookie protection is not enabled, need change"
WRN_C03515_01 = "The parameter net.ipv4.conf.all.log_martians is not set to 1, need change"
WRN_C03515_02 = "The parameter net.ipv4.conf.default.log_martians is not set to 1, need change"
WRN_C03516 = "The tcp_timestamps is enabled, need change"
WRN_C03517 = "The TIME WAIT tcp fin timeout is greater than 60, need change"
WRN_C03518 = "The SYN_RECV state queue number (tcp_max_syn_backlog) is less than 256, need change"
WRN_C03519_01 = "The parameter net.ipv4.conf.all.proxy_arp is not set to 0, need change"
WRN_C03519_02 = "The parameter net.ipv4.conf.default.proxy_arp is not set to 0, need change"
WRN_C03520 = "The core dump is not disabled or the core dump storage is not safe, need change"

SUG_C03401 = ("Please remove the write permission of group and other users from the crontab scripts:"
              "</br>chmod og-w <script>")
SUG_C03402 = ("Please enable and start the cron daemon:"
              "</br>systemctl enable crond"
              "</br>systemctl start crond")
SUG_C03403_01 = ("Please enable and start the cron daemon:"
              "</br>systemctl enable crond"
              "</br>systemctl start crond")
SUG_C03403_02 = ("Please set the owner to root and remove the permissions of group and other users:"
              "</br>chown root:root /etc/crontab /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly /etc/cron.d"
              "</br>chmod og-rwx /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly /etc/cron.d")
SUG_C03403_03 = ("Please remove the cron deny files and use the allow files instead:"
              "</br>rm /etc/cron.deny /etc/at.deny")
SUG_C03403_04 = ("Please create the cron allow files with owner root and permission 600:"
              "</br>touch /etc/cron.allow /etc/at.allow"
              "</br>chown root:root /etc/cron.allow /etc/at.allow"
              "</br>chmod 600 /etc/cron.allow /etc/at.allow")
SUG_C03501 = ("Please enable the kernel ASLR:"
              "</br>sysctl -w kernel.randomize_va_space=2")
SUG_C03504 = ("Please remove the nosmap boot option and reboot the system:"
              "</br>vim /etc/default/grub"
              "</br>grub2-mkconfig -o /boot/grub2/grub.cfg")
SUG_C03505 = ("Please remove the nosmep boot option and reboot the system:"
              "</br>vim /etc/default/grub"
              "</br>grub2-mkconfig -o /boot/grub2/grub.cfg")
SUG_C03506 = ("Please make the system ignore ICMP broadcast requests:"
              "</br>sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=1")
SUG_C03507_01 = ("Please disable accepting ICMP redirects:"
              "</br>sysctl -w net.ipv4.conf.all.accept_redirects=0")
SUG_C03507_02 = ("Please disable accepting ICMPv6 redirects:"
              "</br>sysctl -w net.ipv6.conf.all.accept_redirects=0")
SUG_C03507_03 = ("Please disable accepting secure ICMP redirects:"
              "</br>sysctl -w net.ipv4.conf.all.secure_redirects=0")
SUG_C03507_04 = ("Please disable accepting secure ICMP redirects on new interfaces:"
              "</br>sysctl -w net.ipv4.conf.default.secure_redirects=0")
SUG_C03508_01 = ("Please disable sending ICMP redirects:"
              "</br>sysctl -w net.ipv4.conf.all.send_redirects=0")
SUG_C03508_02 = ("Please disable sending ICMP redirects on new interfaces:"
              "</br>sysctl -w net.ipv4.conf.default.send_redirects=0")
SUG_C03510 = ("Please make the system ignore bogus ICMP error responses:"
              "</br>sysctl -w net.ipv4.icmp_ignore_bogus_error_responses=1")
SUG_C03511_01 = ("Please enable the reverse path filtering:"
              "</br>sysctl -w net.ipv4.conf.all.rp_filter=1")
SUG_C03511_02 = ("Please enable the reverse path filtering on new interfaces:"
              "</br>sysctl -w net.ipv4.conf.default.rp_filter=1")
SUG_C03512_01 = ("Please disable the IPv4 forwarding:"
              "</br>sysctl -w net.ipv4.ip_forward=0")
SUG_C03512_02 = ("Please disable the IPv6 forwarding:"
              "</br>sysctl -w net.ipv6.conf.all.forwarding=0")
SUG_C03513_01 = ("Please disable the IP source routing:"
              "</br>sysctl -w net.ipv4.conf.all.accept_source_route=0")
SUG_C03513_02 = ("Please disable the IP source routing on new interfaces:"
              "</br>sysctl -w net.ipv4.conf.default.accept_source_route=0")
SUG_C03513_03 = ("Please disable the IPv6 source routing:"
              "</br>sysctl -w net.ipv6.conf.all.accept_source_route=0")
SUG_C03513_04 = ("Please disable the IPv6 source routing on new interfaces:"
              "</br>sysctl -w net.ipv6.conf.default.accept_source_route=0")
SUG_C03514 = ("Please enable the TCP SYN cookie protection:"
              "</br>sysctl -w net.ipv4.tcp_syncookies=1")
SUG_C03515_01 = ("Please enable logging of the spoofing, source-routed and redirect packets:"
              "</br>sysctl -w net.ipv4.conf.all.log_martians=1")
SUG_C03515_02 = ("Please enable logging of the spoofing, source-routed and redirect packets on new interfaces:"
              "</br>sysctl -w net.ipv4.conf.default.log_martians=1")
SUG_C03516 = ("Please disable the tcp_timestamps:"
              "</br>sysctl -w net.ipv4.tcp_timestamps=0")
SUG_C03517 = ("Please set the tcp_fin_timeout correctly:"
              "</br>sysctl -w net.ipv4.tcp_fin_timeout=60")
SUG_C03518 = ("Please set the tcp_max_syn_backlog correctly:"
              "</br>sysctl -w net.ipv4.tcp_max_syn_backlog=256")
SUG_C03519_01 = ("Please disable the ARP proxy:"
              "</br>sysctl -w net.ipv4.conf.all.proxy_arp=0")
SUG_C03519_02 = ("Please disable the ARP proxy on new interfaces:"
              "</br>sysctl -w net.ipv4.conf.default.proxy_arp=0")
SUG_C03520 = ("Please disable the core dump:"
              "</br>echo \"* hard core 0\" >> /etc/security/limits.conf"
              "</br>sysctl -w fs.suid_dumpable=0")

# 4 审计与日志
WRN_C04101_01 = "The audit or audit-libs software is not installed in your Linux System"
WRN_C04101_02 = "The auditd service is not enabled in your Linux System"
WRN_C04101_03 = "The auditd service is not active in your Linux System"
WRN_C04102_01 = "The max_log_file_action of audit log rotate is not set to ROTATE or KEEP_LOGS in /etc/audit/auditd.conf"
WRN_C04102_02 = "The num_logs of audit log rotate is not set correctly in /etc/audit/auditd.conf"
WRN_C04111 = "The max_log_file of audit log size limit is not configured correctly in /etc/audit/auditd.conf"
WRN_C04201_01 = "The rsyslog software is not installed in your Linux System"
WRN_C04201_02 = "The rsyslog service is not enabled in your Linux System"
WRN_C04201_03 = "The rsyslog service is not active in your Linux System"
WRN_C04202 = "The auth events log is not recorded in /etc/rsyslog.conf"
WRN_C04203 = "The cron service log is not recorded in /etc/rsyslog.conf"
WRN_C04206 = "The rsyslog dump journald log is not configured in /etc/rsyslog.conf"
WRN_C04207_01 = "The rsyslog log rotate paths are not configured completely in /etc/logrotate.d/rsyslog"
WRN_C04207_02 = "The rsyslog log rotate params are not configured completely in /etc/logrotate.d/rsyslog"

SUG_C04101_01 = ("Please install the audit and audit-libs software:"
              "</br>dnf install -y audit audit-libs")
SUG_C04101_02 = ("Please enable and start the auditd service:"
              "</br>systemctl enable auditd.service"
              "</br>systemctl start auditd.service")
SUG_C04101_03 = ("Please enable and start the auditd service:"
              "</br>systemctl enable auditd.service"
              "</br>systemctl start auditd.service")
SUG_C04102_01 = ("Please set the max_log_file_action in /etc/audit/auditd.conf:"
              "</br>max_log_file_action = ROTATE"
              "</br>service auditd restart")
SUG_C04102_02 = ("Please set the num_logs in /etc/audit/auditd.conf:"
              "</br>num_logs = 5"
              "</br>service auditd restart")
SUG_C04111 = ("Please set the max_log_file in /etc/audit/auditd.conf:"
              "</br>max_log_file = 8"
              "</br>service auditd restart")
SUG_C04201_01 = ("Please install the rsyslog software:"
              "</br>dnf install -y rsyslog")
SUG_C04201_02 = ("Please enable and start the rsyslog service:"
              "</br>systemctl enable rsyslog.service"
              "</br>systemctl start rsyslog.service")
SUG_C04201_03 = ("Please enable and start the rsyslog service:"
              "</br>systemctl enable rsyslog.service"
              "</br>systemctl start rsyslog.service")
SUG_C04202 = ("Please add the auth config in /etc/rsyslog.conf:"
              "</br>authpriv.*                                         /var/log/secure"
              "</br>systemctl restart rsyslog.service")
SUG_C04203 = ("Please add the cron config in /etc/rsyslog.conf:"
              "</br>cron.*                                                  /var/log/cron"
              "</br>systemctl restart rsyslog.service")
SUG_C04206 = ("Please add the imjournal module config in /etc/rsyslog.conf:"
              "</br>module(load=\"imjournal\" StateFile=\"/run/log/imjournal.state\")"
              "</br>systemctl restart rsyslog.service")
SUG_C04207_01 = ("Please add the log file paths in /etc/logrotate.d/rsyslog:"
              "</br>/var/log/cron /var/log/maillog /var/log/messages /var/log/secure /var/log/spooler")
SUG_C04207_02 = ("Please add the rotate params in /etc/logrotate.d/rsyslog:"
              "</br>maxage 365"
              "</br>rotate 30"
              "</br>compress"
              "</br>size +4096k")

WRN_no_file = "does not exist in the system"
SUG_no_file = "does not exist in the system, check if this system is running normally"
