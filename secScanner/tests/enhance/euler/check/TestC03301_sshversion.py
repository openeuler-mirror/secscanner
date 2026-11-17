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
import secScanner.enhance.euler.check.C03301_sshversion as C03301_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03301_sshversion import C03301_sshversion

CONFIG_FILE = "/etc/ssh/sshd_config"
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


class TestC03301_sshversion(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03301_sshversion.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.logger')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.Display')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.InsertSection')
    def test_protocol_1_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {CONFIG_FILE: ['Port 22\n', 'Protocol 1\n']}
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        C03301_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C03301_sshversion()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of ssh protocol version in sshd config file")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC03301\n")])
        mock_logger.warning.assert_any_call("WRN_C03301: %s", WRN_C03301)
        mock_logger.warning.assert_any_call("SUG_C03301: %s", SUG_C03301)
        mock_Display.assert_called_once_with("- Wrong set of ssh protocol version in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03301_sshversion.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.logger')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.Display')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.InsertSection')
    def test_protocol_2_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {CONFIG_FILE: ['Port 22\n', 'Protocol 2\n']}
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C03301_sshversion()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of ssh protocol version in sshd config file")
        self.assertEqual(written, [])
        self.assertEqual([item for item in opened if item[0] == RESULT], [])
        mock_logger.info.assert_called_once_with("Check set of ssh protocol version in sshd config file")
        mock_Display.assert_called_once_with("- Check set of ssh protocol version in sshd config file", "OK")

    @patch('secScanner.enhance.euler.check.C03301_sshversion.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.logger')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.Display')
    @patch('secScanner.enhance.euler.check.C03301_sshversion.InsertSection')
    def test_sshd_config_missing_skipping(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：sshd_config 不存在时应记录结果文件并跳过检查"""
        # Mock test setup.
        mock_exists.return_value = False
        written, opened = [], []
        C03301_module.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open({}, written, opened)):
            C03301_sshversion()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of ssh protocol version in sshd config file")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC03301\n")])
        mock_logger.warning.assert_any_call("WRN_C03301: /etc/ssh/sshd_config " + WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C03301: /etc/ssh/sshd_config " + SUG_no_file)
        mock_Display.assert_called_once_with("- Config file: /etc/ssh/sshd_config not found...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()
