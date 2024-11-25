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
from secScanner.enhance.euler.check.C0207_passwdGroupexists import *
import secScanner


class TestC0207_passwdGroupexists(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.InsertSection')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.logger')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 和 /etc/group 都不存在
        mock_exists.side_effect = [False, False]

        # 调用测试函数
        C0207_passwdGroupexists()
        mock_InsertSection.assert_called_once_with("check if all groups in /etc/passwd exist")
        mock_logger.warning.assert_any_call("WRN_C0207_02: %s", WRN_C0207_02)
        mock_logger.warning.assert_any_call("SUG_C0207_02: %s", SUG_C0207_02)
        mock_display.assert_called_with("- file /etc/group or /etc/passwd does not exist...", "WARNING")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.InsertSection')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.logger')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_group_file_not_found(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd存在，/etc/group 不存在
        mock_exists.side_effect = [True, False]

        # 调用测试函数
        C0207_passwdGroupexists()
        mock_InsertSection.assert_called_once_with("check if all groups in /etc/passwd exist")
        mock_logger.warning.assert_any_call("WRN_C0207_02: %s", WRN_C0207_02)
        mock_logger.warning.assert_any_call("SUG_C0207_02: %s", SUG_C0207_02)
        mock_display.assert_called_once_with("- file /etc/group or /etc/passwd does not exist...", "WARNING")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.InsertSection')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.logger')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_file_not_found(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd不存在，/etc/group 存在
        mock_exists.side_effect = [False, True]

        # 调用测试函数
        C0207_passwdGroupexists()
        mock_InsertSection.assert_called_once_with("check if all groups in /etc/passwd exist")
        mock_logger.warning.assert_any_call("WRN_C0207_02: %s", WRN_C0207_02)
        mock_logger.warning.assert_any_call("SUG_C0207_02: %s", SUG_C0207_02)
        mock_display.assert_called_once_with("- file /etc/group or /etc/passwd does not exist...", "WARNING")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.InsertSection')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.logger')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.check_group_in_group')
    def test_group_found(self, mock_check_group_in_group, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd和/etc/group 都存在
        mock_exists.side_effect = [True, True]
        # 模拟 /etc/passwd 中的组都存在
        mock_check_group_in_group.return_value = True
        # 调用测试函数
        C0207_passwdGroupexists()
        mock_InsertSection.assert_called_once_with("check if all groups in /etc/passwd exist")
        mock_logger.info.assert_any_call("All groups in /etc/passwd exist, checking ok")
        mock_display.assert_called_once_with("- Check if all groups in /etc/passwd exist...", "OK")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.InsertSection')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.logger')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.check_group_in_group')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.get_user_groups_from_passwd')
    def test_group_not_found(self, mock_get_user_groups_from_passwd, mock_check_group_in_group, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.side_effect = [True, True]
        mock_get_user_groups_from_passwd.return_value = [("user1", "group1"), ("user2", "group2")]
        mock_check_group_in_group.side_effect = [False, False]
        # 调用测试函数
        C0207_passwdGroupexists()
        username = []
        username.append("user1")
        username.append("user2")
        mock_InsertSection.assert_called_once_with("check if all groups in /etc/passwd exist")
        mock_logger.warning.assert_any_call(f"WRN_C0207_01: Group for user [{username}] not found")
        mock_logger.warning.assert_any_call("SUG_C0207_01: %s", SUG_C0207_01)
        mock_display.assert_called_once_with("- Check if all groups in /etc/passwd exist...", "WARNING")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.InsertSection')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.logger')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.check_group_in_group')
    @patch('secScanner.enhance.euler.check.C0207_passwdGroupexists.get_user_groups_from_passwd')
    def test_user1_group_not_found(self, mock_get_user_groups_from_passwd, mock_check_group_in_group, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.side_effect = [True, True]
        mock_get_user_groups_from_passwd.return_value = [("user1", "group1"), ("user2", "group2")]
        mock_check_group_in_group.side_effect = [False, True]
        # 调用测试函数
        C0207_passwdGroupexists()
        username = []
        username.append("user1")
        mock_InsertSection.assert_any_call("check if all groups in /etc/passwd exist")
        mock_logger.warning.assert_any_call(f"WRN_C0207_01: Group for user [{username}] not found")
        mock_logger.warning.assert_any_call("SUG_C0207_01: %s", SUG_C0207_01)
        mock_display.assert_called_once_with("- Check if all groups in /etc/passwd exist...", "WARNING")

if __name__ == "__main__":
    unittest.main()