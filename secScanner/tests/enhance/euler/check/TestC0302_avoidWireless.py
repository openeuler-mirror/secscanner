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
from secScanner.enhance.euler.check.C0302_avoidWireless import C0302_avoidWireless
import secScanner

class TestC0302_avoidWireless(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.InsertSection')
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.logger')
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_cmd_failed(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.return_value = (1, "")
        C0302_avoidWireless()
        mock_InsertSection.assert_any_call("Check avoid using wireless network")
        mock_logger.warning.assert_any_call("Excute cmd: 'nmcli radio all' failed")
        mock_display.assert_any_call("- A error occurred while checking nmcli raido...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.InsertSection')
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.logger')
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_wireless_disabled(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟无线网络已禁用的情况
        mock_getstatusoutput.return_value = (0, "WIFI-HW  WIFI     WWAN-HW  WWAN\nenabled  disabled  enabled  disabled")
        C0302_avoidWireless()
        mock_InsertSection.assert_any_call("Check avoid using wireless network")
        mock_logger.info.assert_any_call("Checking wireless network is disabled")
        mock_display.assert_any_call("- Checking wireless network is disabled", "OK")
    
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.InsertSection')
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.logger')
    @patch('secScanner.enhance.euler.check.C0302_avoidWireless.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_wireless_enabled(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟无线网络已启用的情况
        mock_getstatusoutput.return_value = (0, "WIFI-HW  WIFI     WWAN-HW  WWAN\nenabled  enabled   enabled  enabled")
        secScanner.enhance.euler.check.C0302_avoidWireless.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        C0302_avoidWireless()
        mock_InsertSection.assert_any_call("Check avoid using wireless network")
        mock_logger.warning.assert_any_call("WRN_C0302: %s", WRN_C0302)
        mock_logger.warning.assert_any_call("SUG_C0302: %s", SUG_C0302)
        mock_display.assert_any_call("- Wireless network should be banned...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()