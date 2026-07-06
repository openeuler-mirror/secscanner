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
from secScanner.enhance.euler.check.C0339_banTCPforwarding import C0339_banTCPforwarding
import secScanner


class TestC0339_banTCPforwarding(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.InsertSection')
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.logger')
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    @patch('os.path.exists')
    def test_file_not_exists(self, mock_exists, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        config_file = "/etc/ssh/sshd_config"
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0339_banTCPforwarding.RESULT_FILE = "result_file_path"  # Mock test setup.
        # Mock test setup.
        C0339_banTCPforwarding()
        mock_InsertSection.assert_any_call("Check set of AllowTcpForwarding in sshd config file")
        mock_logger.warning.assert_any_call(f"WRN_C0339: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0339: {config_file} {SUG_no_file}")
        mock_display.assert_any_call(f"- Config file: {config_file} not found...", "SKIPPING")
        mock_open.assert_called_with("result_file_path", "a")
    
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.InsertSection')
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.logger')
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    @patch('os.path.exists')
    def test_set_correct(self, mock_exists, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_exists.return_value = True
        mock_getstatusoutput.side_effect = [(0, "AllowTcpForwarding no"), (1, "")]
        # Mock test setup.
        C0339_banTCPforwarding()
        mock_InsertSection.assert_any_call("Check set of AllowTcpForwarding in sshd config file")
        mock_logger.info.assert_any_call("Check set of AllowTcpForwarding in sshd config file")
        mock_display.assert_any_call("- Check set of AllowTcpForwarding in sshd config file", "OK")
        
    
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.InsertSection')
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.logger')
    @patch('secScanner.enhance.euler.check.C0339_banTCPforwarding.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    @patch('os.path.exists')
    def test_set_incorrect(self, mock_exists, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_exists.return_value = True
        mock_getstatusoutput.side_effect = [(1, ""), (0, "AllowTcpForwarding yes")]
        secScanner.enhance.euler.check.C0339_banTCPforwarding.RESULT_FILE = "result_file_path"  # Mock test setup.
        C0339_banTCPforwarding()
        mock_InsertSection.assert_any_call("Check set of AllowTcpForwarding in sshd config file")
        mock_logger.warning.assert_any_call("WRN_C0339: %s", WRN_C0339)
        mock_logger.warning.assert_any_call("SUG_C0339: %s", SUG_C0339)
        mock_display.assert_any_call("- Wrong set of AllowTcpForwarding in sshd config file...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()