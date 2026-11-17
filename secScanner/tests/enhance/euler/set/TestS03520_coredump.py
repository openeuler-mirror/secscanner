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
import logging
from secScanner.enhance.euler.set.S03520_coredump import S03520_coredump  # Mock test setup.

class TestS03520_coredump(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03520_coredump.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03520_coredump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.makedirs')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.set.S03520_coredump.Display')
    @patch('secScanner.enhance.euler.set.S03520_coredump.logger')
    @patch('secScanner.enhance.euler.set.S03520_coredump.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_exists, mock_makedirs,
                                      mock_add_bak_file, mock_copy2, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03520_coredump()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_coredump')
        mock_InsertSection.assert_called_once_with("Set the core dump disabled...")
        mock_Display.assert_called_once_with("- Skip set core dump disabled due to config file...", "SKIPPING")
        mock_run.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03520_coredump.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03520_coredump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.makedirs')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.set.S03520_coredump.Display')
    @patch('secScanner.enhance.euler.set.S03520_coredump.logger')
    @patch('secScanner.enhance.euler.set.S03520_coredump.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_success_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                  mock_InsertSection, mock_exists, mock_makedirs,
                                  mock_add_bak_file, mock_copy2, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=0)

        # Mock test setup.
        S03520_coredump()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_coredump')
        mock_InsertSection.assert_called_once_with("Set the core dump disabled...")
        mock_file.assert_any_call("/etc/security/limits.conf", "a")
        mock_file.assert_any_call("/etc/sysctl.d/secscanner.conf", "a")
        mock_file().write.assert_any_call("\n* hard core 0\n")
        mock_file().write.assert_any_call("fs.suid_dumpable=0" + "\n")
        mock_run.assert_called_once_with(["sysctl", "-w", "fs.suid_dumpable=0"], capture_output=True)
        mock_logger.info.assert_any_call("Set core dump disabled finish")
        mock_Display.assert_called_once_with("- Set core dump disabled...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03520_coredump.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03520_coredump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.makedirs')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.set.S03520_coredump.Display')
    @patch('secScanner.enhance.euler.set.S03520_coredump.logger')
    @patch('secScanner.enhance.euler.set.S03520_coredump.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="*    hard    core    0\n")
    def test_already_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                       mock_InsertSection, mock_exists, mock_makedirs,
                                       mock_add_bak_file, mock_copy2, mock_run):
        """边界：limits.conf 已存在 hard core 0 配置，应跳过设置"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S03520_coredump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the core dump disabled...")
        mock_logger.info.assert_called_once_with("Core dump is already disabled in limits.conf")
        mock_Display.assert_called_once_with("- Core dump has already been disabled...", "SKIPPING")
        mock_run.assert_not_called()
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03520_coredump.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03520_coredump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.makedirs')
    @patch('secScanner.enhance.euler.set.S03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.set.S03520_coredump.Display')
    @patch('secScanner.enhance.euler.set.S03520_coredump.logger')
    @patch('secScanner.enhance.euler.set.S03520_coredump.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                          mock_InsertSection, mock_exists, mock_makedirs,
                          mock_add_bak_file, mock_copy2, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False
        mock_makedirs.side_effect = OSError("permission denied")

        # Mock test setup.
        S03520_coredump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the core dump disabled...")
        mock_logger.warning.assert_called_once_with("Set core dump disabled failed")
        mock_Display.assert_called_once_with("- Set core dump disabled...", "FAILED")
        mock_run.assert_not_called()

if __name__ == '__main__':
    unittest.main()
