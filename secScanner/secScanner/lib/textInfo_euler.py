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
                "</br>#echo '\s' > /etc/issue"
                "</br>#echo 'Kernel \r on an \m' >> /etc/issue"
                "</br>2、可根据实际需要修改该文件的内容。"
                "</br>补充操作说明：/etc/issue文件不为空")
SUG_C0228_03 = ("1、修改文件/etc/issue.net的内容，如没有该文件，则创建它，并写入内容。"
                "</br>#touch /etc/issue.net "
                "</br>#echo '\s' > /etc/issue.net"
                "</br>#echo 'Kernel \r on an \m' >> /etc/issue.net"
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
WRN_no_file = "does not exist in the system"
SUG_no_file = "does not exist in the system, check if this system is running normally"
