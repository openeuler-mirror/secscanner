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
from unittest.mock import patch, MagicMock
import logging
from secScanner.enhance.euler.set.S03501_aslr import S03501_aslr

SYSCTL_CONF = "/etc/sysctl.d/secscanner.conf"


def _make_run(stdout=b"", returncode=0):
    result = MagicMock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestS03501_aslr(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03501_aslr._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.set.S03501_aslr.Display')
    @patch('secScanner.enhance.euler.set.S03501_aslr.logger')
    @patch('secScanner.enhance.euler.set.S03501_aslr.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_persist, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03501_aslr()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_aslr')
        mock_InsertSection.assert_called_once_with("Set the kernel ASLR enabled...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set kernel.randomize_va_space due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03501_aslr._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.set.S03501_aslr.Display')
    @patch('secScanner.enhance.euler.set.S03501_aslr.logger')
    @patch('secScanner.enhance.euler.set.S03501_aslr.seconf.get')
    def test_already_enabled_skipping_boundary(self, mock_seconf_get, mock_logger, mock_Display,
                                               mock_InsertSection, mock_persist, mock_run):
        """边界：当前值已为 2，无需再次写入，应只查询一次并跳过"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = _make_run(b"kernel.randomize_va_space = 2\n")

        # Mock test setup.
        S03501_aslr()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_aslr')
        mock_InsertSection.assert_called_once_with("Set the kernel ASLR enabled...")
        mock_run.assert_called_once_with(['sysctl', 'kernel.randomize_va_space'], capture_output=True)
        mock_persist.assert_not_called()
        mock_logger.info.assert_called_once_with("kernel.randomize_va_space already set to 2")
        mock_Display.assert_called_once_with("- kernel.randomize_va_space has already been set to 2...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03501_aslr._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.set.S03501_aslr.Display')
    @patch('secScanner.enhance.euler.set.S03501_aslr.logger')
    @patch('secScanner.enhance.euler.set.S03501_aslr.seconf.get')
    def test_set_aslr_finished(self, mock_seconf_get, mock_logger, mock_Display,
                               mock_InsertSection, mock_persist, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _make_run(b"kernel.randomize_va_space = 0\n"),
            _make_run(b"kernel.randomize_va_space = 2\n", 0),
        ]

        # Mock test setup.
        S03501_aslr()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the kernel ASLR enabled...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(["sysctl", "-w", "kernel.randomize_va_space=2"], capture_output=True)
        mock_persist.assert_called_once_with([("kernel.randomize_va_space", "kernel.randomize_va_space=2")])
        mock_logger.info.assert_any_call("Set kernel.randomize_va_space finish")
        mock_Display.assert_called_once_with("- Set kernel.randomize_va_space=2...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03501_aslr._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.set.S03501_aslr.Display')
    @patch('secScanner.enhance.euler.set.S03501_aslr.logger')
    @patch('secScanner.enhance.euler.set.S03501_aslr.seconf.get')
    def test_set_aslr_failed(self, mock_seconf_get, mock_logger, mock_Display,
                             mock_InsertSection, mock_persist, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _make_run(b"kernel.randomize_va_space = 1\n"),
            _make_run(b"sysctl: permission denied\n", 1),
        ]

        # Mock test setup.
        S03501_aslr()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the kernel ASLR enabled...")
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_logger.warning.assert_called_once_with("Set kernel.randomize_va_space failed")
        mock_Display.assert_called_once_with("- Set kernel.randomize_va_space=2...", "FAILED")

if __name__ == '__main__':
    unittest.main()
