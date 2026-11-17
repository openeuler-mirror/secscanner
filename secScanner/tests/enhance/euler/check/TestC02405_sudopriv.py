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
import secScanner.enhance.euler.check.C02405_sudopriv as C02405_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02405_sudopriv import C02405_sudopriv  # Mock test setup.

SUDOERS_FILE = '/etc/sudoers'


def make_file(content=''):
    handle = MagicMock()
    handle.read.return_value = content
    handle.readlines.return_value = content.splitlines(True)
    handle.__iter__.return_value = iter(content.splitlines(True))
    handle.__enter__.return_value = handle
    file_mock = MagicMock()
    file_mock.__enter__.return_value = handle
    file_mock.__exit__.return_value = False
    return file_mock


def open_router(files):
    def _open(path, *args, **kwargs):
        if path not in files:
            raise AssertionError("unexpected open call: %s" % path)
        return files[path]
    return _open


class TestC02405_sudopriv(unittest.TestCase):

    def setUp(self):
        C02405_module.RESULT_FILE = 'check_result.relt'

    @patch('secScanner.enhance.euler.check.C02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.logger')
    def test_not_compliant_warning(self, mock_logger, mock_Display, mock_InsertSection,
                                   mock_open, mock_exists, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, 'package sudo is not installed')
        result = make_file('')
        mock_open.side_effect = open_router({
            SUDOERS_FILE: make_file("Defaults env_reset\nDefaults secure_path = /sbin:/bin\n"),
            'check_result.relt': result,
        })
        mock_exists.return_value = True

        # Mock test setup.
        C02405_sudopriv()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that normal users can run privileged programs through sudo")
        mock_getstatusoutput.assert_called_once_with('rpm -q sudo')
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_with('\nC02405\n')
        self.assertEqual(result.__enter__.return_value.write.call_count, 3)
        mock_logger.warning.assert_any_call("WRN_C02405_01: %s", WRN_C02405_01)
        mock_logger.warning.assert_any_call("SUG_C02405_01: %s", SUG_C02405_01)
        mock_logger.warning.assert_any_call("WRN_C02405_02: %s", WRN_C02405_02)
        mock_logger.warning.assert_any_call("SUG_C02405_02: %s", SUG_C02405_02)
        mock_logger.warning.assert_any_call("WRN_C02405_03: %s", WRN_C02405_03)
        mock_logger.warning.assert_any_call("SUG_C02405_03: %s", SUG_C02405_03)
        mock_Display.assert_any_call("- sudo is not installed...", "WARNING")
        mock_Display.assert_any_call("- No (root) sudo rule set in /etc/sudoers...", "WARNING")
        mock_Display.assert_any_call("- No wheel group sudo rule set in /etc/sudoers...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.logger')
    def test_compliant_ok(self, mock_logger, mock_Display, mock_InsertSection,
                          mock_open, mock_exists, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, 'sudo-1.9.5p2-1.oe2203')
        sudoers = make_file("Defaults env_reset\nroot ALL=(ALL) ALL\n%wheel ALL=(ALL) ALL\n")
        mock_open.side_effect = open_router({SUDOERS_FILE: sudoers})
        mock_exists.return_value = True

        # Mock test setup.
        C02405_sudopriv()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that normal users can run privileged programs through sudo")
        mock_open.assert_called_once_with(SUDOERS_FILE, 'r')
        mock_logger.info.assert_any_call("sudo is installed, checking ok")
        mock_logger.info.assert_any_call("(root) sudo rule is configured in /etc/sudoers, checking ok")
        mock_logger.info.assert_any_call("wheel group sudo rule is enabled in /etc/sudoers, checking ok")
        mock_Display.assert_any_call("- Has sudo installed...", "OK")
        mock_Display.assert_any_call("- Has (root) sudo rule set in /etc/sudoers...", "OK")
        mock_Display.assert_any_call("- Has wheel group sudo rule set in /etc/sudoers...", "OK")
        self.assertEqual(mock_logger.warning.call_count, 0)

    @patch('secScanner.enhance.euler.check.C02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.logger')
    def test_sudoers_missing_skipping(self, mock_logger, mock_Display, mock_InsertSection,
                                      mock_open, mock_exists, mock_getstatusoutput):
        """边界：/etc/sudoers 不存在时应跳过并写入结果文件"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, 'sudo-1.9.5p2-1.oe2203')
        result = make_file('')
        mock_open.side_effect = open_router({'check_result.relt': result})
        mock_exists.return_value = False

        # Mock test setup.
        C02405_sudopriv()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that normal users can run privileged programs through sudo")
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC02405\n')
        mock_logger.warning.assert_any_call("WRN_C02405: /etc/sudoers %s", WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02405: /etc/sudoers %s", SUG_no_file)
        mock_Display.assert_any_call("- Config file: /etc/sudoers not found...", "SKIPPING")

    @patch('secScanner.enhance.euler.check.C02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.check.C02405_sudopriv.logger')
    def test_root_rule_only_warning(self, mock_logger, mock_Display, mock_InsertSection,
                                    mock_open, mock_exists, mock_getstatusoutput):
        """边界：仅配置 root 规则而缺少 wheel 规则，只应告警 wheel 一项"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, 'sudo-1.9.5p2-1.oe2203')
        result = make_file('')
        mock_open.side_effect = open_router({
            SUDOERS_FILE: make_file("root ALL=(ALL) ALL\n"),
            'check_result.relt': result,
        })
        mock_exists.return_value = True

        # Mock test setup.
        C02405_sudopriv()

        # Mock test setup.
        result.__enter__.return_value.write.assert_called_once_with('\nC02405\n')
        mock_logger.warning.assert_any_call("WRN_C02405_03: %s", WRN_C02405_03)
        mock_logger.warning.assert_any_call("SUG_C02405_03: %s", SUG_C02405_03)
        mock_Display.assert_any_call("- Has (root) sudo rule set in /etc/sudoers...", "OK")
        mock_Display.assert_any_call("- No wheel group sudo rule set in /etc/sudoers...", "WARNING")


if __name__ == '__main__':
    unittest.main()
