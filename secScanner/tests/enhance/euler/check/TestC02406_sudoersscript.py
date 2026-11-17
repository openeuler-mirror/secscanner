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
import secScanner.enhance.euler.check.C02406_sudoersscript as C02406_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02406_sudoersscript import C02406_sudoersscript  # Mock test setup.

SUDOERS_FILE = '/etc/sudoers'
SCRIPT_FILE = '/usr/local/bin/tool.sh'


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


def stat_info(mode, uid):
    info = MagicMock()
    info.st_mode = mode
    info.st_uid = uid
    return info


class TestC02406_sudoersscript(unittest.TestCase):

    def setUp(self):
        C02406_module.RESULT_FILE = 'check_result.relt'

    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.logger')
    def test_writable_script_warning(self, mock_logger, mock_Display, mock_InsertSection,
                                     mock_open, mock_exists, mock_stat):
        # Mock test setup.
        result = make_file('')
        mock_open.side_effect = open_router({
            SUDOERS_FILE: make_file("%wheel ALL=(ALL) " + SCRIPT_FILE + "\n"),
            'check_result.relt': result,
        })
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SCRIPT_FILE)
        mock_stat.return_value = stat_info(0o777, 1000)

        # Mock test setup.
        C02406_sudoersscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the scripts in sudoers are not writable by low privilege users")
        mock_open.assert_any_call(SUDOERS_FILE, 'r')
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC02406\n')
        mock_stat.assert_called_once_with(SCRIPT_FILE)
        mock_logger.warning.assert_any_call("WRN_C02406_01: %s", WRN_C02406_01)
        mock_logger.warning.assert_any_call("SUG_C02406_01: %s", SUG_C02406_01)
        mock_Display.assert_called_once_with(
            "- Scripts %s are writable by low privilege users..." % SCRIPT_FILE, "WARNING")

    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.logger')
    def test_script_not_writable_ok(self, mock_logger, mock_Display, mock_InsertSection,
                                    mock_open, mock_exists, mock_stat):
        # Mock test setup.
        mock_open.side_effect = open_router({
            SUDOERS_FILE: make_file("%wheel ALL=(ALL) " + SCRIPT_FILE + "\n"),
        })
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SCRIPT_FILE)
        mock_stat.return_value = stat_info(0o755, 0)

        # Mock test setup.
        C02406_sudoersscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the scripts in sudoers are not writable by low privilege users")
        mock_logger.info.assert_called_once_with(
            "no script in sudoers is writable by low privilege users, checking ok")
        mock_Display.assert_called_once_with(
            "- No script in sudoers is writable by low privilege users...", "OK")
        self.assertEqual(mock_logger.warning.call_count, 0)

    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.logger')
    def test_sudoers_missing_skipping(self, mock_logger, mock_Display, mock_InsertSection,
                                      mock_open, mock_exists, mock_stat):
        """边界：/etc/sudoers 不存在时应跳过并写入结果文件"""
        # Mock test setup.
        result = make_file('')
        mock_open.side_effect = open_router({'check_result.relt': result})
        mock_exists.return_value = False

        # Mock test setup.
        C02406_sudoersscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the scripts in sudoers are not writable by low privilege users")
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC02406\n')
        mock_stat.assert_not_called()
        mock_logger.warning.assert_any_call("WRN_C02406: /etc/sudoers %s", WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02406: /etc/sudoers %s", SUG_no_file)
        mock_Display.assert_called_once_with("- Config file: /etc/sudoers not found...", "SKIPPING")

    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.check.C02406_sudoersscript.logger')
    def test_script_missing_ok(self, mock_logger, mock_Display, mock_InsertSection,
                               mock_open, mock_exists, mock_stat):
        """边界：sudoers 中的脚本路径不存在时不应判定为不合规"""
        # Mock test setup.
        mock_open.side_effect = open_router({
            SUDOERS_FILE: make_file("%wheel ALL=(ALL) /usr/local/bin/missing.sh\n"),
        })
        mock_exists.side_effect = lambda path: path == SUDOERS_FILE

        # Mock test setup.
        C02406_sudoersscript()

        # Mock test setup.
        mock_stat.assert_not_called()
        mock_Display.assert_called_once_with(
            "- No script in sudoers is writable by low privilege users...", "OK")


if __name__ == '__main__':
    unittest.main()
