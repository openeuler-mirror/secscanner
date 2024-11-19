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
from secScanner.enhance.euler.check.C0210_GIDunique import C0210_GIDunique
import secScanner


class TestC0210_GIDunique(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0210_GIDunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0210_GIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0210_GIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_gid_unique(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/group 文件存在且 GID 唯一
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, '')
        # 调用测试函数
        C0210_GIDunique()
        mock_InsertSection.assert_called_with("Check if GID is unique")
        mock_logger.info.assert_called_once_with("Confirm GID uniqueness, checking OK")
        mock_display.assert_called_once_with("- Confirm GID uniqueness...", "OK")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0210_GIDunique.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0210_GIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0210_GIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_gid_not_unique(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟 /etc/group 文件存在但 GID 不唯一
        mock_getstatusoutput.return_value = (0, '1000')
        secScanner.enhance.euler.check.C0210_GIDunique.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0210_GIDunique()
        mock_logger.warning.assert_any_call("WRN_C0210_01: %s", WRN_C0210_01)
        mock_logger.warning.assert_any_call("SUG_C0210_01: %s", SUG_C0210_01)
        mock_display.assert_called_once_with("- Duplicate GID ['1000']...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
if __name__ == '__main__':
    unittest.main()