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


import unittest
from unittest.mock import patch, mock_open
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0209_userNameunique import C0209_userNameunique
import secScanner
# 模拟文件内容
passwd_content_duplicate = """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
lp:x:6:12:man:/var/cache/man:/usr/sbin/nologin"""

passwd_content_no_duplicate = """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin"""

class TestC0209_userNameunique(unittest.TestCase):

            
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0209_userNameunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0209_userNameunique.logger')
    @patch('secScanner.enhance.euler.check.C0209_userNameunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_file_not_exist(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件不存在的情况
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0209_userNameunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0209_userNameunique()
        mock_InsertSection.assert_called_with("Check if the account is unique")
        mock_logger.warning.assert_any_call("WRN_C0209_02: %s", WRN_C0209_02)
        mock_logger.warning.assert_any_call("SUG_C0209_02: %s", SUG_C0209_02)
        mock_display.assert_any_call("- file /etc/passwd dose not exist...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")



    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0209_userNameunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0209_userNameunique.logger')
    @patch('secScanner.enhance.euler.check.C0209_userNameunique.Display')
    @patch('builtins.open', new_callable=mock_open, read_data=passwd_content_duplicate)
    def test_username_unique_duplicate(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件存在的情况
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0209_userNameunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0209_userNameunique()
        mock_InsertSection.assert_called_with("Check if the account is unique")
        mock_logger.warning.assert_any_call("WRN_C0209_01: %s", WRN_C0209_01)
        mock_logger.warning.assert_any_call("SUG_C0209_01: %s", SUG_C0209_01)
        mock_display.assert_any_call("- Duplicate users found in /etc/passwd ...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
    
if __name__ == '__main__':
    unittest.main()