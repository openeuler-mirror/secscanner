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
from secScanner.enhance.euler.check.C0336_delSSHpresets import C0336_delSSHpresets
import secScanner


class TestC0336_delSSHpresets(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0336_delSSHpresets.InsertSection')
    @patch('secScanner.enhance.euler.check.C0336_delSSHpresets.logger')
    @patch('secScanner.enhance.euler.check.C0336_delSSHpresets.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_cmd_fail(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.return_value = (1, "")
        C0336_delSSHpresets()
        mock_InsertSection.assert_any_call("Check ssh presets in /home/ /root/")
        mock_logger.warning.assert_any_call("Excute find cmd: 'find /home/ /root/ -name authorized_keys' failed")
        mock_display.assert_any_call("- A error occurred while checking ssh presets...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0336_delSSHpresets.InsertSection')
    @patch('secScanner.enhance.euler.check.C0336_delSSHpresets.logger')
    @patch('secScanner.enhance.euler.check.C0336_delSSHpresets.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_not_found(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.return_value = (0, "")
        C0336_delSSHpresets()
        mock_InsertSection.assert_any_call("Check ssh presets in /home/ /root/")
        mock_logger.info.assert_any_call("Not found ssh presets in /home/ /root/")
        mock_display.assert_any_call("- Not found ssh presets in /home/ /root/...", "OK")

if __name__ == '__main__':
    unittest.main()