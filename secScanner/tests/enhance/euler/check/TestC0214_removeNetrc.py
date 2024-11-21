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
from secScanner.enhance.euler.check.C0214_removeNetrc import C0214_removeNetrc
import secScanner

class TestC0214_removeNetrc(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_with_netrc_file(self, mock_walk, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟存在.netrc文件
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], [".netrc"]), ("/home/user2", [], [])]
        secScanner.enhance.euler.check.C0214_removeNetrc.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0214_removeNetrc()
        mock_InsertSection.assert_any_call("Confirm the existence of the .netrc file in the Home directory")
        mock_logger.warning.assert_any_call("WRN_C0214_01: %s", WRN_C0214_01)
        mock_logger.warning.assert_any_call("SUG_C0214_01: %s", SUG_C0214_01)
        mock_display.assert_called_once_with("- At least one .netrc file in the Home directory ...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_without_netrc_file(self, mock_walk, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟不存在.netrc文件
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], []), ("/home/user2", [], [])]
        # 调用测试函数
        C0214_removeNetrc()
        mock_InsertSection.assert_any_call("Confirm the existence of the .netrc file in the Home directory")
        mock_logger.info.assert_any_call("Confirm the existence of the .netrc file in the Home directory, checking ok")
        mock_display.assert_called_once_with("- check if the .netrc file in the Home directory...", "OK")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_fail_obtain_user_home_list(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件存在
        mock_exists.return_value = True
        # 模拟读取home目录失败
        mock_getstatusoutput.return_value = (1, "")
        secScanner.enhance.euler.check.C0214_removeNetrc.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0214_removeNetrc()
        mock_InsertSection.assert_any_call("Confirm the existence of the .netrc file in the Home directory")
        mock_logger.warning.assert_any_call("WRN_C0214_02: %s", WRN_C0214_02)
        mock_logger.warning.assert_any_call("SUG_C0214_01: %s", SUG_C0214_01)
        mock_display.assert_called_once_with("- Failed to obtain passwd user's home list ...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.check.C0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_file_not_exists(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件不存在
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0214_removeNetrc.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0214_removeNetrc()
        mock_InsertSection.assert_any_call("Confirm the existence of the .netrc file in the Home directory")
        mock_logger.warning.assert_any_call("WRN_C0214_03: %s", WRN_C0214_03)
        mock_logger.warning.assert_any_call("SUG_C0214_02: %s", SUG_C0214_02)
        mock_display.assert_called_once_with("- file /etc/passwd does not exist...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
        
if __name__ == '__main__':
    unittest.main()