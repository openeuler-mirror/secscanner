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
from secScanner.enhance.level3.check.C131_sshActive import C131_sshActive

class TestC131_sshActive(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C131_sshActive.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', side_effect=[(0, 'active'), (0, 'enabled')])
    @patch('secScanner.enhance.level3.check.C131_sshActive.logger')
    @patch('secScanner.enhance.level3.check.C131_sshActive.Display')
    def test_ssh_enabled_and_running(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C131_sshActive()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("SSH service enabled and running")
        mock_display.assert_called_with("- SSH service enabled and running...", "OK")

    @patch('secScanner.enhance.level3.check.C131_sshActive.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', side_effect=[(0, 'active'), (0, 'disabled')])
    @patch('secScanner.enhance.level3.check.C131_sshActive.logger')
    @patch('secScanner.enhance.level3.check.C131_sshActive.Display')
    def test_ssh_running_not_enabled(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C131_sshActive()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("SSH service is running but not enabled")
        mock_display.assert_called_with("- SSH service is running but not enabled...", "OK")

    @patch('secScanner.enhance.level3.check.C131_sshActive.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, 'inactive'))
    @patch('secScanner.enhance.level3.check.C131_sshActive.logger')
    @patch('secScanner.enhance.level3.check.C131_sshActive.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_ssh_startup_failed(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C131_sshActive()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C131_01: %s", WRN_C131_01)
        mock_logger.warning.assert_any_call("SUG_C131_01: %s", SUG_C131_01)
        mock_display.assert_called_with("- The SSH service startup failed...", "WARNING")

    @patch('secScanner.enhance.level3.check.C131_sshActive.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(1, 'error'))
    @patch('secScanner.enhance.level3.check.C131_sshActive.logger')
    @patch('secScanner.enhance.level3.check.C131_sshActive.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_check_service_failed(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C131_sshActive()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C131_02: %s", WRN_C131_02)
        mock_logger.warning.assert_any_call("SUG_C131_02: %s", SUG_C131_02)
        mock_display.assert_called_with("- Failed to check if the service is available", "WARNING")

    @patch('secScanner.enhance.level3.check.C131_sshActive.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C131_sshActive.logger')
    @patch('secScanner.enhance.level3.check.C131_sshActive.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_service_file_not_exist(self, mock_file, mock_display, mock_logger, mock_exists, mock_insert):
        # 运行测试的函数
        C131_sshActive()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C131_03: %s", WRN_C131_03)
        mock_logger.warning.assert_any_call("SUG_C131_03: %s", SUG_C131_03)
        mock_display.assert_called_with("- file /usr/lib/systemd/system/sshd.service dose not exist...", "WARNING")

if __name__ == '__main__':
    unittest.main()
