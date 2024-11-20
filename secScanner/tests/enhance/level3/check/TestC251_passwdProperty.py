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
from secScanner.enhance.level3.check.C251_passwdProperty import C251_passwdProperty

class TestC251_passwdProperty(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C251_passwdProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw-r--r-- 1 root root 123456 Jul 10 10:00 /etc/passwd"))
    @patch('secScanner.enhance.level3.check.C251_passwdProperty.logger')
    @patch('secScanner.enhance.level3.check.C251_passwdProperty.Display')
    def test_passwd_property_correct(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C251_passwdProperty()

        # 检查预期的日志信息是否已正确记录
        mock_display.assert_called_with("- check if /etc/passwd property is 644 ...", "OK")

    @patch('secScanner.enhance.level3.check.C251_passwdProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw------- 1 root root 123456 Jul 10 10:00 /etc/passwd"))
    @patch('secScanner.enhance.level3.check.C251_passwdProperty.logger')
    @patch('secScanner.enhance.level3.check.C251_passwdProperty.Display')
    def test_passwd_property_incorrect(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C251_passwdProperty()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C251: %s", WRN_C251)
        mock_logger.warning.assert_any_call("SUG_C251: %s", SUG_C251)
        mock_display.assert_called_with("- Check if /etc/passwd property is not 644...", "WARNING")

if __name__ == '__main__':
    unittest.main()
