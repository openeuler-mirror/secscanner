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
import secScanner
import secScanner.enhance.euler.check.C03504_smap as C03504_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03504_smap import C03504_smap

CPUINFO = "/proc/cpuinfo"
CMDLINE = "/proc/cmdline"
RESULT = "check_result.relt"


def _make_open(files, written, opened):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.read.return_value = files.get(path, "")
        else:
            handle.write.side_effect = lambda data: written.append((path, data))
        return handle
    return _open


class TestC03504_smap(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.check.C03504_smap.Display')
    @patch('secScanner.enhance.euler.check.C03504_smap.logger')
    def test_smap_disabled_by_nosmap_warning(self, mock_logger, mock_Display, mock_InsertSection):
        # Mock test setup.
        files = {
            CPUINFO: "processor\t: 0\nflags\t\t: fpu vme smap\n",
            CMDLINE: "BOOT_IMAGE=/vmlinuz nosmap root=/dev/mapper/openeuler-root ro\n",
        }
        written, opened = [], []

        # Mock test setup.
        C03504_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C03504_smap()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMAP is enabled")
        self.assertIn((CPUINFO, "r", None), opened)
        self.assertIn((CMDLINE, "r", None), opened)
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC03504\n")])
        mock_logger.warning.assert_any_call("WRN_C03504: %s", WRN_C03504)
        mock_logger.warning.assert_any_call("SUG_C03504: %s", SUG_C03504)
        mock_Display.assert_called_once_with("- The kernel SMAP is disabled by nosmap boot option...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.check.C03504_smap.Display')
    @patch('secScanner.enhance.euler.check.C03504_smap.logger')
    def test_smap_enabled_ok(self, mock_logger, mock_Display, mock_InsertSection):
        # Mock test setup.
        files = {
            CPUINFO: "processor\t: 0\nflags\t\t: fpu vme smap\n",
            CMDLINE: "BOOT_IMAGE=/vmlinuz root=/dev/mapper/openeuler-root ro\n",
        }
        written, opened = [], []

        # Mock test setup.
        C03504_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C03504_smap()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMAP is enabled")
        self.assertNotIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [])
        mock_logger.info.assert_called_once_with("The kernel SMAP is enabled")
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether the kernel SMAP is enabled...", "OK")

    @patch('secScanner.enhance.euler.check.C03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.check.C03504_smap.Display')
    @patch('secScanner.enhance.euler.check.C03504_smap.logger')
    def test_cpu_without_smap_skipping_boundary(self, mock_logger, mock_Display, mock_InsertSection):
        """边界：cpuinfo 中 smap 仅作为子串出现（非常规 flag），不应读取 cmdline 并判定为跳过"""
        # Mock test setup.
        files = {
            CPUINFO: "processor\t: 0\nflags\t\t: fpu vme nosmapflag\n",
            CMDLINE: "BOOT_IMAGE=/vmlinuz nosmap\n",
        }
        written, opened = [], []

        # Mock test setup.
        C03504_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C03504_smap()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel SMAP is enabled")
        self.assertEqual([entry[0] for entry in opened], [CPUINFO])
        self.assertEqual(written, [])
        mock_logger.info.assert_called_once_with("The CPU does not support SMAP, skip this check")
        mock_Display.assert_called_once_with("- The CPU does not support SMAP, skip this check...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
