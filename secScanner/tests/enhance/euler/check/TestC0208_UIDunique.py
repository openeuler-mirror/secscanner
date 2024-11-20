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
from secScanner.enhance.euler.check.C0208_UIDunique import C0208_UIDunique
import secScanner


class TestC0208_UIDunique(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_file_not_exist(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件不存在的情况
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0208_UIDunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0208_UIDunique()
        mock_InsertSection.assert_called_with("Check if UID is unique")
        mock_logger.warning.assert_any_call("WRN_C0208_04: %s", WRN_C0208_04)
        mock_logger.warning.assert_any_call("SUG_C0208_04: %s", SUG_C0208_04)
        mock_display.assert_any_call("- file /etc/passwd dose not exist...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")



    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_fail_retrieve_uids(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件存在的情况
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0208_UIDunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        mock_getstatusoutput.return_value = (1,'')
        # 调用测试函数
        C0208_UIDunique()
        mock_InsertSection.assert_called_with("Check if UID is unique")
        mock_logger.warning.assert_any_call("WRN_C0208_03: %s", WRN_C0208_03)
        mock_logger.warning.assert_any_call("SUG_C0208_03: %s", SUG_C0208_03)
        mock_display.assert_any_call("- Failed to retrieve UID information...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_UIDunique_no_duplicate_uids(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件存在的情况
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0208_UIDunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 模拟uuid不重复
        mock_getstatusoutput.return_value = (0, "  1 1000\n  1 1001\n 1 1002")
        # 调用测试函数
        C0208_UIDunique()
        mock_InsertSection.assert_called_with("Check if UID is unique")
        mock_logger.info.assert_any_call("Confirm UID uniqueness, checking OK")
        mock_display.assert_any_call("- Confirm UID uniqueness...", "OK")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0208_UIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_UIDunique_duplicate_uids(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/passwd 文件存在的情况
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0208_UIDunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 模拟uuid重复
        mock_getstatusoutput.side_effect = [(0, "  1 1000\n  1 1001\n 2 1002"),
                                            (0,"uuid_duplicate_username")]
        # 调用测试函数
        C0208_UIDunique()
        mock_InsertSection.assert_called_with("Check if UID is unique")
        mock_logger.warning.assert_any_call("WRN_C0208_01: %s", WRN_C0208_01)
        mock_logger.warning.assert_any_call("SUG_C0208_01: %s", SUG_C0208_01)
        mock_display.assert_any_call("- Duplicate UID (1002): uuid_duplicate_username...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()