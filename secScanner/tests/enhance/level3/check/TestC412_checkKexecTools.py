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
from secScanner.enhance.level3.check.C412_checkKexecTools import C412_checkKexecTools

class TestC412_checkKexecTools(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C412_checkKexecTools.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, "kexec-tools-2.0.20-14.el7.x86_64"))
    @patch('secScanner.enhance.level3.check.C412_checkKexecTools.logger')
    @patch('secScanner.enhance.level3.check.C412_checkKexecTools.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_kexec_tools_installed(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C412_checkKexecTools()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C412: %s", WRN_C412)
        mock_logger.warning.assert_any_call("SUG_C412: %s", SUG_C412)
        mock_display.assert_called_with("- Check the  Kexec-tools software is installed...", "WARNING")

    @patch('secScanner.enhance.level3.check.C412_checkKexecTools.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, "package kexec-tools is not installed"))
    @patch('secScanner.enhance.level3.check.C412_checkKexecTools.logger')
    @patch('secScanner.enhance.level3.check.C412_checkKexecTools.Display')
    def test_kexec_tools_not_installed(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C412_checkKexecTools()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("The Kexec-tools status is: package kexec-tools is not installed")
        mock_display.assert_called_with("- Check the Kexec-tools software is uninstall...", "OK")

if __name__ == '__main__':
    unittest.main()
