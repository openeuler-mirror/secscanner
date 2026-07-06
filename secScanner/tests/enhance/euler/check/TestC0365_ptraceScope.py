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
import secScanner
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0365_ptraceScope import C0365_ptraceScope

class TestC0365_ptraceScope(unittest.TestCase):
    
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.logger')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_ptraceScope_set_correctly(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        
        mock_exists.side_effect = [True, True]  # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, "kernel.yama.ptrace_scope=2"),
                                            (0, "kernel.yama.ptrace_scope=2")]  # Mock test setup.
        # Mock test setup.
        C0365_ptraceScope()
        mock_InsertSection.assert_called_once_with("Check set of kernel.yama.ptrace_scope in sysctl config file")
        mock_logger.info.assert_any_call("Check set of kernel.yama.ptrace_scope in sysctl config file")
        mock_logger.info.assert_any_call("Check set of kernel.yama.ptrace_scope in sysctl.d/*")
        mock_display.assert_any_call("- Check set of kernel.yama.ptrace_scope in sysctl config file", "OK")
        mock_display.assert_any_call("- Check set of kernel.yama.ptrace_scope in sysctl.d/*", "OK")
    
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.logger')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_ptraceScope_set_incorrectly(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        # Mock test setup.
        secScanner.enhance.euler.check.C0365_ptraceScope.RESULT_FILE = "result_file_path"  # Mock test setup.
        # Mock test setup.
        mock_getsize.return_value = 0  # Mock test setup.

        mock_exists.side_effect = [True, True]  # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, "kernel.yama.ptrace_scope=1"),
                                            (0, "kernel.yama.ptrace_scope=1")]  # Mock test setup.
        # Mock test setup.
        C0365_ptraceScope()
        mock_InsertSection.assert_called_once_with("Check set of kernel.yama.ptrace_scope in sysctl config file")
        mock_logger.warning.assert_any_call("WRN_C0365: %s", WRN_C0365)
        mock_logger.warning.assert_any_call("SUG_C0365: %s", SUG_C0365)
        mock_display.assert_any_call("- Wrong set of kernel.yama.ptrace_scope in sysctl config file...", "WARNING")
        mock_display.assert_any_call("- Wrong set of kernel.yama.ptrace_scope in sysctl.d/*...", "WARNING")
        mock_file.assert_any_call("result_file_path", "a+")  # Mock test setup.
    
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.logger')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_ptraceScope_not_set(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):

        mock_exists.side_effect = [True, True]  # Mock test setup.
        mock_getstatusoutput.return_value = [(1, ""),
                                             (1, "")]  # Mock test setup.
        # Mock test setup.
        C0365_ptraceScope()
        mock_InsertSection.assert_called_once_with("Check set of kernel.yama.ptrace_scope in sysctl config file")
        mock_display.assert_any_call("- Not set of kernel.yama.ptrace_scope in sysctl config file...", "WARNING")
        mock_display.assert_any_call("- Not set of kernel.yama.ptrace_scope in sysctl.d/*...", "WARNING")

    
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.logger')
    @patch('secScanner.enhance.euler.check.C0365_ptraceScope.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        # Mock test setup.
        secScanner.enhance.euler.check.C0365_ptraceScope.RESULT_FILE = "result_file_path"  # Mock test setup.
        # Mock test setup.
        mock_getsize.return_value = 0  # Mock test setup.
        config_file = "/etc/sysctl.conf"
        config_d = "/etc/sysctl.d"
        mock_exists.side_effect = [False, False]  # Mock test setup.
        # Mock test setup.
        C0365_ptraceScope()
        mock_InsertSection.assert_called_once_with("Check set of kernel.yama.ptrace_scope in sysctl config file")
        mock_logger.warning.assert_any_call(f"WRN_C0365: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"WRN_C0365: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0365: {config_d} {SUG_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0365: {config_d} {SUG_no_file}")
        mock_display.assert_any_call(f"- Config file: {config_file} not found...", "SKIPPING")     
        mock_display.assert_any_call(f"- Config file: {config_d} not found...", "SKIPPING")     
        mock_file.assert_any_call("result_file_path", "a+")  # Mock test setup.

if __name__ == '__main__':
    unittest.main()