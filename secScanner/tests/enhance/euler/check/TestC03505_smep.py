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
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03505_smep import C03505_smep  # Mock test setup.

CPU_WITH_SMEP = "processor\t: 0\nflags\t\t: fpu vme smep ssbd\n"
CPU_WITHOUT_SMEP = "processor\t: 0\nflags\t\t: fpu vme ssbd\n"


def _open_side_effect(cpu_data, cmd_data):
    cpu_handle = mock_open(read_data=cpu_data).return_value
    cmd_handle = mock_open(read_data=cmd_data).return_value
    result_handle = mock_open().return_value

    def _open(path, *args, **kwargs):
        if path == "/proc/cpuinfo":
            return cpu_handle
        if path == "/proc/cmdline":
            return cmd_handle
        return result_handle

    return _open, result_handle


class TestC03505_smep(unittest.TestCase):

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03505_smep.logger')
    @patch('secScanner.enhance.euler.check.C03505_smep.Display')
    @patch('secScanner.enhance.euler.check.C03505_smep.InsertSection')
    def test_nosmep_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_file):
        """不合规：CPU 支持 SMEP 但启动参数含 nosmep，应 WARNING 并写入 RESULT_FILE"""
        # Mock test setup.
        side_effect, result_handle = _open_side_effect(CPU_WITH_SMEP, "ro quiet nosmep crashkernel=512M")
        mock_file.side_effect = side_effect
        secScanner.enhance.euler.check.C03505_smep.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMEP is enabled")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        result_handle.write.assert_called_once_with("\nC03505\n")
        mock_logger.warning.assert_any_call("WRN_C03505: %s", WRN_C03505)
        mock_logger.warning.assert_any_call("SUG_C03505: %s", SUG_C03505)
        mock_Display.assert_called_once_with("- The kernel SMEP is disabled by nosmep boot option...", "WARNING")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03505_smep.logger')
    @patch('secScanner.enhance.euler.check.C03505_smep.Display')
    @patch('secScanner.enhance.euler.check.C03505_smep.InsertSection')
    def test_smep_enabled_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_file):
        """合规：CPU 支持 SMEP 且无 nosmep，应 OK 且不写 RESULT_FILE"""
        # Mock test setup.
        side_effect, result_handle = _open_side_effect(CPU_WITH_SMEP, "ro quiet crashkernel=512M")
        mock_file.side_effect = side_effect
        secScanner.enhance.euler.check.C03505_smep.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMEP is enabled")
        result_handle.write.assert_not_called()
        mock_logger.info.assert_called_once_with("The kernel SMEP is enabled")
        mock_Display.assert_called_once_with("- Check whether the kernel SMEP is enabled...", "OK")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03505_smep.logger')
    @patch('secScanner.enhance.euler.check.C03505_smep.Display')
    @patch('secScanner.enhance.euler.check.C03505_smep.InsertSection')
    def test_cpu_without_smep_skipping(self, mock_InsertSection, mock_Display, mock_logger, mock_file):
        """边界：CPU 不支持 SMEP 时不读取 cmdline，直接 SKIPPING"""
        # Mock test setup.
        side_effect, result_handle = _open_side_effect(CPU_WITHOUT_SMEP, "ro quiet nosmep")
        mock_file.side_effect = side_effect
        secScanner.enhance.euler.check.C03505_smep.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMEP is enabled")
        self.assertEqual(mock_file.call_count, 1)
        mock_file.assert_called_once_with("/proc/cpuinfo", "r")
        result_handle.write.assert_not_called()
        mock_logger.info.assert_called_once_with("The CPU does not support SMEP, skip this check")
        mock_Display.assert_called_once_with("- The CPU does not support SMEP, skip this check...", "SKIPPING")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03505_smep.logger')
    @patch('secScanner.enhance.euler.check.C03505_smep.Display')
    @patch('secScanner.enhance.euler.check.C03505_smep.InsertSection')
    def test_nosmep_uppercase_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_file):
        """边界：nosmep 大小写混写也应被识别为不合规"""
        # Mock test setup.
        side_effect, result_handle = _open_side_effect(CPU_WITH_SMEP, "ro quiet NoSMEP")
        mock_file.side_effect = side_effect
        secScanner.enhance.euler.check.C03505_smep.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMEP is enabled")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        result_handle.write.assert_called_once_with("\nC03505\n")
        mock_Display.assert_called_once_with("- The kernel SMEP is disabled by nosmep boot option...", "WARNING")

if __name__ == '__main__':
    unittest.main()
