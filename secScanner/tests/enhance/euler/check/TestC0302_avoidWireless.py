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

if __name__ == '__main__':
    unittest.main()