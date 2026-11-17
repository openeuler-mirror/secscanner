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
from secScanner.enhance.euler.set.S03505_smep import S03505_smep  # Mock test setup.

CPU_WITH_SMEP = "processor\t: 0\nflags\t\t: fpu vme smep ssbd\n"
CPU_WITHOUT_SMEP = "processor\t: 0\nflags\t\t: fpu vme ssbd\n"
GRUB_FILE = "/boot/grub2/grub.cfg"
GRUB_CONTENT = "linux /vmlinuz ro nosmep quiet crashkernel=512M\n"


def _open_side_effect(cpu_data, cmd_data, grub_data):
    cpu_handle = mock_open(read_data=cpu_data).return_value
    cmd_handle = mock_open(read_data=cmd_data).return_value
    grub_read_handle = mock_open(read_data=grub_data).return_value
    grub_write_handle = mock_open().return_value

    def _open(path, mode="r", *args, **kwargs):
        if path == "/proc/cpuinfo":
            return cpu_handle
        if path == "/proc/cmdline":
            return cmd_handle
        if path == GRUB_FILE and "w" in mode:
            return grub_write_handle
        return grub_read_handle

    return _open, grub_write_handle


class TestS03505_smep(unittest.TestCase):

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S03505_smep.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03505_smep.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03505_smep.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03505_smep.logger')
    @patch('secScanner.enhance.euler.set.S03505_smep.Display')
    @patch('secScanner.enhance.euler.set.S03505_smep.InsertSection')
    @patch('secScanner.enhance.euler.set.S03505_smep.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                     mock_exists, mock_copy2, mock_add_bak_file, mock_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03505_smep()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_smep')
        mock_InsertSection.assert_called_once_with("Set the kernel SMEP enabled...")
        mock_Display.assert_called_once_with("- Skip set kernel SMEP due to config file...", "SKIPPING")
        mock_file.assert_not_called()

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S03505_smep.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03505_smep.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03505_smep.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03505_smep.logger')
    @patch('secScanner.enhance.euler.set.S03505_smep.Display')
    @patch('secScanner.enhance.euler.set.S03505_smep.InsertSection')
    @patch('secScanner.enhance.euler.set.S03505_smep.seconf.get')
    def test_remove_nosmep_finished(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                    mock_exists, mock_copy2, mock_add_bak_file, mock_file):
        """配置为 yes 且 grub 配置存在，应移除 nosmep 并 FINISHED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = lambda path: path == GRUB_FILE
        side_effect, grub_write_handle = _open_side_effect(CPU_WITH_SMEP, "ro quiet nosmep", GRUB_CONTENT)
        mock_file.side_effect = side_effect

        # Mock test setup.
        S03505_smep()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_smep')
        mock_InsertSection.assert_called_once_with("Set the kernel SMEP enabled...")
        mock_copy2.assert_called_once_with(GRUB_FILE, GRUB_FILE + "_bak")
        mock_add_bak_file.assert_called_once_with(GRUB_FILE + "_bak")
        written_lines = grub_write_handle.writelines.call_args[0][0]
        self.assertEqual(len(written_lines), 1)
        self.assertNotIn("nosmep", written_lines[0])
        self.assertIn("quiet", written_lines[0])
        mock_logger.info.assert_any_call("Remove nosmep boot option finish")
        mock_Display.assert_called_once_with("- Remove nosmep boot option from grub config...", "FINISHED")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S03505_smep.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03505_smep.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03505_smep.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03505_smep.logger')
    @patch('secScanner.enhance.euler.set.S03505_smep.Display')
    @patch('secScanner.enhance.euler.set.S03505_smep.InsertSection')
    @patch('secScanner.enhance.euler.set.S03505_smep.seconf.get')
    def test_grub_not_found_failed(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                   mock_exists, mock_copy2, mock_add_bak_file, mock_file):
        """配置为 yes 且存在 nosmep，但所有 grub 配置均不存在，应 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False
        side_effect, grub_write_handle = _open_side_effect(CPU_WITH_SMEP, "ro quiet nosmep", "")
        mock_file.side_effect = side_effect

        # Mock test setup.
        S03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the kernel SMEP enabled...")
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        grub_write_handle.writelines.assert_not_called()
        mock_logger.warning.assert_called_once_with("Grub config file not found")
        mock_Display.assert_called_once_with("- Remove nosmep boot option from grub config...", "FAILED")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S03505_smep.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03505_smep.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03505_smep.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03505_smep.logger')
    @patch('secScanner.enhance.euler.set.S03505_smep.Display')
    @patch('secScanner.enhance.euler.set.S03505_smep.InsertSection')
    @patch('secScanner.enhance.euler.set.S03505_smep.seconf.get')
    def test_cpu_not_support_skipping(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                      mock_exists, mock_copy2, mock_add_bak_file, mock_file):
        """边界：CPU 不支持 SMEP 时直接 SKIPPING，不修改 grub"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        side_effect, grub_write_handle = _open_side_effect(CPU_WITHOUT_SMEP, "ro quiet nosmep", GRUB_CONTENT)
        mock_file.side_effect = side_effect

        # Mock test setup.
        S03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the kernel SMEP enabled...")
        mock_file.assert_called_once_with("/proc/cpuinfo", "r")
        mock_copy2.assert_not_called()
        grub_write_handle.writelines.assert_not_called()
        mock_logger.info.assert_called_once_with("The CPU does not support SMEP, skip this set")
        mock_Display.assert_called_once_with("- The CPU does not support SMEP, skip this set...", "SKIPPING")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S03505_smep.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03505_smep.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03505_smep.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03505_smep.logger')
    @patch('secScanner.enhance.euler.set.S03505_smep.Display')
    @patch('secScanner.enhance.euler.set.S03505_smep.InsertSection')
    @patch('secScanner.enhance.euler.set.S03505_smep.seconf.get')
    def test_already_enabled_skipping(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                      mock_exists, mock_copy2, mock_add_bak_file, mock_file):
        """边界：启动参数不含 nosmep 时不修改 grub，直接 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        side_effect, grub_write_handle = _open_side_effect(CPU_WITH_SMEP, "ro quiet", GRUB_CONTENT)
        mock_file.side_effect = side_effect

        # Mock test setup.
        S03505_smep()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the kernel SMEP enabled...")
        mock_copy2.assert_not_called()
        grub_write_handle.writelines.assert_not_called()
        mock_logger.info.assert_called_once_with("The kernel SMEP is already enabled")
        mock_Display.assert_called_once_with("- The kernel SMEP has already been enabled...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
