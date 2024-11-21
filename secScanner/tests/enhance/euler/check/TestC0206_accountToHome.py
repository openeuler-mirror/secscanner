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
from secScanner.enhance.euler.check.C0206_accountToHome import C0206_accountToHome
import secScanner


class TestC0206_accountToHome(unittest.TestCase):
   
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_file_not_found(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 不存在
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0206_accountToHome.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0206_accountToHome()
        mock_InsertSection.assert_called_once_with("check if account has its own home directory")
        mock_logger.warning.assert_any_call("WRN_C0206_05: %s", WRN_C0206_05)
        mock_logger.warning.assert_any_call("SUG_C0206_02: %s", SUG_C0206_02)
        mock_display.assert_called_with("- file /etc/passwd not exists...", "SKIPPING")
        mock_open.assert_any_call("result_file_path", "a")  # 检查是否尝试写入文件
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(1, ""))
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_failed_to_read_passwd(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 存在, 读取 /etc/passwd 失败
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0206_accountToHome.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0206_accountToHome()
        mock_InsertSection.assert_called_once_with("check if account has its own home directory")
        mock_logger.warning.assert_any_call("WRN_C0206_04: %s", WRN_C0206_04)
        mock_logger.warning.assert_any_call("SUG_C0206_01: %s", SUG_C0206_01)
        mock_display.assert_called_with("- Failed to obtain passwd user list ...", "FAILED")
        mock_open.assert_any_call("result_file_path", "a")  # 检查是否尝试写入文件
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, "user1:x:1000:1000::/home/user1:/bin/bash"))
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_no_home_directory(self, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟用户的home目录不存在
        mock_exists.return_value = True
        mock_isdir.return_value = False
        secScanner.enhance.euler.check.C0206_accountToHome.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0206_accountToHome()
        mock_InsertSection.assert_called_once_with("check if account has its own home directory")
        mock_logger.warning.assert_any_call("WRN_C0206_01: %s", WRN_C0206_01)
        mock_logger.warning.assert_any_call("SUG_C0206_01: %s", SUG_C0206_01)
        mock_display.assert_called_with("- At least one account does not have a home folder ...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")  # 检查是否尝试写入文件
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_incorrect_home_directory_owner(self, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟用户的home目录不匹配
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getstatusoutput.side_effect = [
            (0, "user1:x:1000:1000::/home/user1:/bin/bash"),
            (0, "drwxr-xr-x 2 otheruser user1 4096 May 14  2021 /home/user1")  # 所有者不匹配
        ]

        secScanner.enhance.euler.check.C0206_accountToHome.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0206_accountToHome()
        mock_InsertSection.assert_called_once_with("check if account has its own home directory")
        mock_logger.warning.assert_any_call("WRN_C0206_02: %s", WRN_C0206_02)
        mock_logger.warning.assert_any_call("SUG_C0206_01: %s", SUG_C0206_01)
        mock_display.assert_called_with("- At least one home directory does not match the user ...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")  # 检查是否尝试写入文件
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_correct_home_directory_and_owner(self, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟用户的home目录匹配
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getstatusoutput.side_effect = [
            (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash"),
            (0, "drwxr-xr-x 2 user1 user1 4096 May 14  2021 /home/user1"),
            (0, "drwxr-xr-x 2 user2 user2 4096 May 14  2021 /home/user2")
        ]

        secScanner.enhance.euler.check.C0206_accountToHome.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0206_accountToHome()
        mock_InsertSection.assert_called_once_with("check if account has its own home directory")
        mock_logger.info.assert_any_call("Confirm that the account has its own home directory, checking ok")
        mock_display.assert_called_with("- check if account has its own home directory...", "OK")
        mock_open.assert_not_called()
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.check.C0206_accountToHome.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_uncorrect_home_directory_and_unowner(self, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟有的用户目录不存在，有的用户目录不匹配
        mock_exists.return_value = True
        mock_isdir.side_effect = [False, True]
        mock_getstatusoutput.side_effect = [
            (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash"),
            (0, "drwxr-xr-x 2 user1 user2 4096 May 14  2021 /home/user2")
        ]

        secScanner.enhance.euler.check.C0206_accountToHome.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0206_accountToHome()
        mock_InsertSection.assert_called_once_with("check if account has its own home directory")
        mock_logger.warning.assert_any_call("WRN_C0206_03: %s", WRN_C0206_03)
        mock_logger.warning.assert_any_call("SUG_C0206_01: %s", SUG_C0206_01)
        mock_display.assert_called_with("- There are issues with the user and their home directory ...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")  # 检查是否尝试写入文件

if __name__ == "__main__":
    unittest.main()