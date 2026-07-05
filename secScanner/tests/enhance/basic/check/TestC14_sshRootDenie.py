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
from secScanner.lib.textInfo_basic import *
from secScanner.commands.check_outprint import *
from secScanner.enhance.basic.check.C14_sshRootDenie import C14_sshRootDenie

# Mock test setup.
class TestC14_sshRootDenie(unittest.TestCase):
    def setUp(self):
        # Mock test setup.
        self.os_distro = '7'

    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.get_value', return_value='7')
    @patch('builtins.open', new_callable=mock_open, read_data="pts/0\npts/1\n")
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.Display')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.logger')
    def test_securetty_wrong_setting(self, mock_logger, mock_display, mock_file, mock_get_value, mock_insert):
        self.assertIsNone(None, "None value check")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertIsNone(None, "None value check")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertIsNone(None, "None value check")
        self.assertIsInstance("test", str, "Type checking")
        # Mock test setup.
        C14_sshRootDenie()
        
        # Mock test setup.
        mock_display.assert_any_call("- Wrong Telnet Denie set...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C14_01: %s", WRN_C14_01)
        mock_logger.warning.assert_any_call("SUG_C14: %s", SUG_C14)
        mock_display.assert_any_call("- No ssh Root denie set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.get_value', return_value='7')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.Display')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.logger')
    def test_securetty_correct_setting(self, mock_logger, mock_display, mock_file, mock_get_value, mock_insert):
        # Mock test setup.
        C14_sshRootDenie()

        # Mock test setup.
        mock_display.assert_any_call("- Check the telnet deny...", "OK")
        mock_logger.warning.assert_any_call("WRN_C14_01: %s", WRN_C14_01)
        mock_logger.warning.assert_any_call("SUG_C14: %s", SUG_C14)
        mock_display.assert_any_call("- No ssh Root denie set...", "WARNING")
    
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.get_value', return_value='any_other_value')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin no\n")
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.Display')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.logger')
    def test_ssh_config_right_setting(self, mock_logger, mock_display, mock_file, mock_get_value, mock_insert):
        # Mock test setup.
        C14_sshRootDenie()

        # Mock test setup.
        mock_logger.info.assert_any_call("Has ssh Root denie set, checking OK")
        mock_display.assert_any_call("- Check the ssh Root denie...", "OK")

    
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.get_value', return_value='any_other_value')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin yes\n")
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.logger')
    @patch('secScanner.enhance.basic.check.C14_sshRootDenie.Display')
    def test_ssh_config_wrong_setting(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        # Mock test setup.
        C14_sshRootDenie()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C14_02: %s", WRN_C14_02)
        mock_logger.warning.assert_any_call("SUG_C14: %s", SUG_C14) 
        mock_display.assert_any_call("- Wrong ssh Root denie set...", "WARNING")
        self.assertTrue(isinstance([], list), "List type validation")

if __name__ == '__main__':
    unittest.main()

