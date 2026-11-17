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
import secScanner.enhance.euler.check.C01112_nosuidmount as C01112_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01112_nosuidmount import C01112_nosuidmount

MOUNT_CMD = 'mount | grep -v "nosuid" | awk -F " " \'{print $3}\''


def make_file(content):
    handle = MagicMock()
    handle.read.return_value = content
    handle.__iter__.return_value = iter(content.splitlines(True))
    handle.__enter__.return_value = handle
    file_mock = MagicMock()
    file_mock.__enter__.return_value = handle
    file_mock.__exit__.return_value = False
    return file_mock


class TestC01112_nosuidmount(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.logger')
    @patch('builtins.open')
    def test_partition_without_nosuid_warning(self, mock_open, mock_logger, mock_Display,
                                              mock_InsertSection, mock_getstatusoutput):
        mock_getstatusoutput.return_value = (0, '/media/usb\n/data\n')
        result = make_file('')
        mock_open.return_value = result
        C01112_module.RESULT_FILE = 'check_result.relt'

        C01112_nosuidmount()

        mock_InsertSection.assert_called_once_with("Check whether the partitions are mounted with nosuid option")
        mock_getstatusoutput.assert_called_once_with(MOUNT_CMD)
        mock_open.assert_called_once_with('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC01112\n')
        mock_logger.warning.assert_any_call('WRN_C01112: %s', WRN_C01112)
        mock_logger.warning.assert_any_call('SUG_C01112: %s', SUG_C01112)
        mock_Display.assert_any_call("- The partition /media/usb is not mounted with nosuid option...", "WARNING")
        mock_Display.assert_any_call("- The partition /data is not mounted with nosuid option...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.logger')
    @patch('builtins.open')
    def test_default_mounts_only_ok(self, mock_open, mock_logger, mock_Display,
                                    mock_InsertSection, mock_getstatusoutput):
        mock_getstatusoutput.return_value = (0, '/\n/boot\n/home\n')
        C01112_module.RESULT_FILE = 'check_result.relt'

        C01112_nosuidmount()

        mock_open.assert_not_called()
        mock_logger.info.assert_called_once_with(
            "All the partitions which need nosuid are mounted with nosuid option, checking ok")
        mock_Display.assert_called_once_with(
            "- Check whether the partitions are mounted with nosuid option...", "OK")

    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.check.C01112_nosuidmount.logger')
    @patch('builtins.open')
    def test_trailing_slash_normalized(self, mock_open, mock_logger, mock_Display,
                                       mock_InsertSection, mock_getstatusoutput):
        """边界：/home/ 去掉尾斜杠后属于默认挂载点，只有 /opt/ 应被判为不合规"""
        mock_getstatusoutput.return_value = (0, '/home/\n/opt/\n')
        result = make_file('')
        mock_open.return_value = result
        C01112_module.RESULT_FILE = 'check_result.relt'

        C01112_nosuidmount()

        result.__enter__.return_value.write.assert_called_once_with('\nC01112\n')
        mock_Display.assert_called_once_with("- The partition /opt is not mounted with nosuid option...", "WARNING")


if __name__ == '__main__':
    unittest.main()
