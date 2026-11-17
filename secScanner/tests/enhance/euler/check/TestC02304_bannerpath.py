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
import secScanner.enhance.euler.check.C02304_bannerpath as C02304_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02304_bannerpath import C02304_bannerpath  # Mock test setup.

CONFIG_FILE = '/etc/ssh/sshd_config'
BANNER_FILE = '/etc/issue.net'


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


class TestC02304_bannerpath(unittest.TestCase):

    def setUp(self):
        C02304_module.RESULT_FILE = 'check_result.relt'

    @patch('secScanner.enhance.euler.check.C02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.logger')
    def test_no_banner_configured_warning(self, mock_logger, mock_Display, mock_InsertSection,
                                          mock_open, mock_exists):
        # Mock test setup.
        config = make_file("Port 22\nPermitRootLogin no\n")
        result = make_file('')
        mock_open.side_effect = open_router({
            CONFIG_FILE: config,
            'check_result.relt': result,
        })
        mock_exists.side_effect = lambda path: path == CONFIG_FILE

        # Mock test setup.
        C02304_bannerpath()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the banner path is configured correctly")
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC02304\n')
        mock_logger.warning.assert_any_call('WRN_C02304_01: %s', WRN_C02304_01)
        mock_logger.warning.assert_any_call('SUG_C02304_01: %s', SUG_C02304_01)
        mock_Display.assert_called_once_with("- No Banner set in /etc/ssh/sshd_config...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.logger')
    def test_banner_file_not_exist_warning(self, mock_logger, mock_Display, mock_InsertSection,
                                           mock_open, mock_exists):
        # Mock test setup.
        config = make_file("Banner %s\n" % BANNER_FILE)
        result = make_file('')
        mock_open.side_effect = open_router({
            CONFIG_FILE: config,
            'check_result.relt': result,
        })
        mock_exists.side_effect = lambda path: path == CONFIG_FILE

        # Mock test setup.
        C02304_bannerpath()

        # Mock test setup.
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC02304\n')
        mock_logger.warning.assert_any_call('WRN_C02304_02: %s', WRN_C02304_02)
        mock_logger.warning.assert_any_call('SUG_C02304_02: %s', SUG_C02304_02)
        mock_Display.assert_called_once_with(
            "- Banner file %s does not exist..." % BANNER_FILE, "WARNING")

    @patch('secScanner.enhance.euler.check.C02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.logger')
    def test_banner_configured_correctly_ok(self, mock_logger, mock_Display, mock_InsertSection,
                                            mock_open, mock_exists):
        # Mock test setup.
        config = make_file("Port 22\nBanner %s\n" % BANNER_FILE)
        mock_open.side_effect = open_router({
            CONFIG_FILE: config,
        })
        mock_exists.return_value = True

        # Mock test setup.
        C02304_bannerpath()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the banner path is configured correctly")
        mock_logger.info.assert_called_once_with("Banner path is configured correctly, checking ok")
        mock_Display.assert_called_once_with(
            "- Has Banner set to %s in /etc/ssh/sshd_config..." % BANNER_FILE, "OK")

    @patch('secScanner.enhance.euler.check.C02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.check.C02304_bannerpath.logger')
    def test_sshd_config_missing_skipping(self, mock_logger, mock_Display, mock_InsertSection,
                                          mock_open, mock_exists):
        """边界：sshd_config 不存在时应跳过并写入结果文件"""
        # Mock test setup.
        result = make_file('')
        mock_open.side_effect = open_router({
            'check_result.relt': result,
        })
        mock_exists.return_value = False

        # Mock test setup.
        C02304_bannerpath()

        # Mock test setup.
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC02304\n')
        mock_logger.warning.assert_any_call("WRN_C02304: %s %s" % (CONFIG_FILE, WRN_no_file))
        mock_logger.warning.assert_any_call("SUG_C02304: %s %s" % (CONFIG_FILE, SUG_no_file))
        mock_Display.assert_called_once_with(
            "- Config file: %s not found..." % CONFIG_FILE, "SKIPPING")


if __name__ == '__main__':
    unittest.main()
