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
import secScanner.enhance.euler.check.C02408_suenv as C02408_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02408_suenv import C02408_suenv

CONFIG_FILE = "/etc/login.defs"
RESULT = "check_result.relt"


def _make_open(files, written, opened):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(files.get(path, []))
        else:
            handle.write.side_effect = lambda data: written.append((path, data))
        return handle
    return _open


def _make_exists(files):
    return lambda path: path in files


class TestC02408_suenv(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02408_suenv.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02408_suenv.logger')
    @patch('secScanner.enhance.euler.check.C02408_suenv.Display')
    @patch('secScanner.enhance.euler.check.C02408_suenv.InsertSection')
    def test_always_set_path_no_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {CONFIG_FILE: ['# comment\n', 'ALWAYS_SET_PATH\tno\n']}
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        C02408_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02408_suenv()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that su command does not inherit the user PATH environment variable")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02408\n")])
        mock_logger.warning.assert_any_call("WRN_C02408_02: %s", WRN_C02408_02)
        mock_logger.warning.assert_any_call("SUG_C02408: %s", SUG_C02408)
        mock_Display.assert_called_once_with("- ALWAYS_SET_PATH is not set to yes in /etc/login.defs...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02408_suenv.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02408_suenv.logger')
    @patch('secScanner.enhance.euler.check.C02408_suenv.Display')
    @patch('secScanner.enhance.euler.check.C02408_suenv.InsertSection')
    def test_always_set_path_yes_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {CONFIG_FILE: ['ALWAYS_SET_PATH\t\tyes\n']}
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02408_suenv()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that su command does not inherit the user PATH environment variable")
        self.assertEqual(written, [])
        self.assertEqual([item for item in opened if item[0] == RESULT], [])
        mock_logger.info.assert_called_once_with("ALWAYS_SET_PATH is set to yes in /etc/login.defs, checking ok")
        mock_Display.assert_called_once_with("- Has ALWAYS_SET_PATH set to yes in /etc/login.defs...", "OK")

    @patch('secScanner.enhance.euler.check.C02408_suenv.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02408_suenv.logger')
    @patch('secScanner.enhance.euler.check.C02408_suenv.Display')
    @patch('secScanner.enhance.euler.check.C02408_suenv.InsertSection')
    def test_commented_always_set_path_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：ALWAYS_SET_PATH 仅出现在注释行时应视为未配置"""
        # Mock test setup.
        files = {CONFIG_FILE: ['#ALWAYS_SET_PATH\tyes\n']}
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        C02408_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02408_suenv()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that su command does not inherit the user PATH environment variable")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02408\n")])
        mock_logger.warning.assert_any_call("WRN_C02408_01: %s", WRN_C02408_01)
        mock_logger.warning.assert_any_call("SUG_C02408: %s", SUG_C02408)
        mock_Display.assert_called_once_with("- No ALWAYS_SET_PATH config set in /etc/login.defs...", "WARNING")


if __name__ == '__main__':
    unittest.main()
