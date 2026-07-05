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
        # Mock test setup.
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true')

        # Mock test setup.
        C0117_prohibitUSBCheck()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- Check whether the prohibition of USB devices is enabled...", "OK")
        mock_logger.info.assert_called_once_with("The prohibition of USB devices is enabled")

    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_usb_prohibition_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        # Mock test setup.
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'')

        # Mock test setup.
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"

        # Mock test setup.
        C0117_prohibitUSBCheck()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0117: %s", WRN_C0117)
        mock_logger.warning.assert_any_call("SUG_C0117: %s", SUG_C0117)
        mock_file.assert_called_once_with("result_file_path", "a")  # Mock test setup.
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_001_stdout_with_trailing_newline_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true\n')
        C0117_prohibitUSBCheck()
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- Check whether the prohibition of USB devices is enabled...", "OK")
        mock_logger.info.assert_called_once_with("The prohibition of USB devices is enabled")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_002_stdout_with_leading_newline_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'\ninstall /bin/true')
        C0117_prohibitUSBCheck()
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- Check whether the prohibition of USB devices is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_003_stdout_with_crlf_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true\r\n')
        C0117_prohibitUSBCheck()
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- Check whether the prohibition of USB devices is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_004_stdout_with_surrounding_spaces_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'  install /bin/true  ')
        C0117_prohibitUSBCheck()
        mock_InsertSection.assert_called_once_with("Check whether the prohibition of USB devices  is enabled")
        mock_Display.assert_called_once_with("- Check whether the prohibition of USB devices is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_005_stdout_only_newline_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'\n')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0117: %s", WRN_C0117)
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_006_stdout_garbage_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'some random output')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
        mock_file.assert_called_once_with("result_file_path", "a")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_007_stdout_install_bin_false_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/false')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0117: %s", WRN_C0117)
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_008_stdout_install_bin_true_uppercase_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'INSTALL /BIN/TRUE')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_009_stdout_partial_match_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true extra')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_010_stdout_install_bin_true_with_tab_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install\t/bin/true')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_Display.assert_called_once_with("- The Prohibition of USB devices is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_011_insert_section_called_once_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true')
        C0117_prohibitUSBCheck()
        self.assertEqual(mock_InsertSection.call_count, 1)
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_012_insert_section_called_once_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        self.assertEqual(mock_InsertSection.call_count, 1)
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_013_logger_warning_not_called_when_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true')
        C0117_prohibitUSBCheck()
        mock_logger.warning.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_014_logger_info_not_called_when_disabled(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        C0117_prohibitUSBCheck()
        mock_logger.info.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_015_display_ok_not_called_when_disabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'')
        secScanner.enhance.euler.check.C0117_prohibitUSBCheck.RESULT_FILE = "result_file_path"
        with patch('builtins.open', mock_open()):
            C0117_prohibitUSBCheck()
        ok_calls = [c for c in mock_Display.call_args_list if "OK" in c.args]
        self.assertEqual(len(ok_calls), 0)
    
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.logger')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.Display')
    @patch('secScanner.enhance.euler.check.C0117_prohibitUSBCheck.InsertSection')
    def test_016_display_warning_not_called_when_enabled(self, mock_InsertSection, mock_Display, mock_logger, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["modprobe", "-n", "-v", "usb-storage"], returncode=0, stdout=b'install /bin/true')
        C0117_prohibitUSBCheck()
        warning_calls = [c for c in mock_Display.call_args_list if "WARNING" in c.args]
        self.assertEqual(len(warning_calls), 0)

if __name__ == '__main__':
    unittest.main()