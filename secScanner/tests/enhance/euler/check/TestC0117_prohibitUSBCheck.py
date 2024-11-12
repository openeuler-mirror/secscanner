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
import subprocess
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0117_prohibitUSBCheck import C0117_prohibitUSBCheck

class TestC0117_prohibitUSBCheck(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_usb_prohibition_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        # 设置模拟返回值
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true')

        # 调用测试函数
        C0117_prohibitUSBCheck()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- Check whether the prohibition of USB devices is enabled...", "OK")
        mock_logger.info.assert_called_once_with("The prohibition of USB devices is enabled")

    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_usb_prohibition_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        # 设置模拟返回值
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'')

        # 假设的全局变量
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"

        # 调用测试函数
        C0117_prohibitUSBCheck()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0117: %s", WRN_C0117)
        mock_logger.warning.assert_any_call("SUG_C0117: %s", SUG_C0117)
        mock_file.assert_called_once_with("result_file_path", "a")  # 检查是否尝试写入文件

if __name__ == '__main__':
    unittest.main()