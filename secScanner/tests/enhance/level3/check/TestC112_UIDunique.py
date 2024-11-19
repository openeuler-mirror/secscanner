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
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C112_UIDunique import C112_UIDunique

class TestC112_UIDunique(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C112_UIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', side_effect=[
        (0, "      1 0\n      1 1\n      1 2"),  # 第一次调用返回没有重复的UID
        (0, "")  # 第二次调用(如果有的话)的返回值
    ])
    @patch('secScanner.enhance.level3.check.C112_UIDunique.logger')
    @patch('secScanner.enhance.level3.check.C112_UIDunique.Display')
    def test_no_duplicate_uids(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C112_UIDunique()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Confirm UID uniqueness, checking OK")
        mock_display.assert_called_with("- Confirm UID uniqueness...", "OK")

    @patch('secScanner.enhance.level3.check.C112_UIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', side_effect=[
        (0, "      1 0\n      2 1000\n      1 2"),  # 第一次调用返回有重复的UID
        (0, "user1\nuser2")  # 第二次调用返回重复UID的用户列表
    ])
    @patch('secScanner.enhance.level3.check.C112_UIDunique.logger')
    @patch('secScanner.enhance.level3.check.C112_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_uids_found(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C112_UIDunique()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C112_01: %s", WRN_C112_01)
        mock_logger.warning.assert_any_call("SUG_C112_01: %s", SUG_C112_01)
        mock_display.assert_called_with("- Duplicate UID (1000): user1 user2...", "WARNING")

    @patch('secScanner.enhance.level3.check.C112_UIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', side_effect=[
        (0, "      1 0\n      2 1000\n      1 2"),  # 第一次调用返回有重复的UID
        (1, "Error")  # 第二次调用失败
    ])
    @patch('secScanner.enhance.level3.check.C112_UIDunique.logger')
    @patch('secScanner.enhance.level3.check.C112_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_failed_to_retrieve_users(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C112_UIDunique()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C112_02: %s", WRN_C112_02)
        mock_logger.warning.assert_any_call("SUG_C112_02: %s", SUG_C112_02)
        mock_display.assert_called_with("- Failed to retrieve users for UID...", "WARNING")


    @patch('secScanner.enhance.level3.check.C112_UIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(1, "Error"))
    @patch('secScanner.enhance.level3.check.C112_UIDunique.logger')
    @patch('secScanner.enhance.level3.check.C112_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_command_execution_failed(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C112_UIDunique()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C112_03: %s", WRN_C112_03)
        mock_logger.warning.assert_any_call("SUG_C112_03: %s", SUG_C112_03)
        mock_display.assert_called_with("- Failed to retrieve UID information...", "WARNING")

    @patch('secScanner.enhance.level3.check.C112_UIDunique.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C112_UIDunique.logger')
    @patch('secScanner.enhance.level3.check.C112_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_file_not_exists(self, mock_file, mock_display, mock_logger, mock_exists, mock_insert):
        # 运行测试的函数
        C112_UIDunique()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C112_04: %s", WRN_C112_04)
        mock_logger.warning.assert_any_call("SUG_C112_04: %s", SUG_C112_04)
        mock_display.assert_called_with("- file /etc/passwd dose not exist...", "WARNING")

if __name__ == '__main__':
    unittest.main()
