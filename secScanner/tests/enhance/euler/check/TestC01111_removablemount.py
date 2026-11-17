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
import secScanner.enhance.euler.check.C01111_removablemount as C01111_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01111_removablemount import C01111_removablemount


def make_file(content):
    handle = MagicMock()
    handle.read.return_value = content
    handle.__iter__.return_value = iter(content.splitlines(True))
    handle.__enter__.return_value = handle
    file_mock = MagicMock()
    file_mock.__enter__.return_value = handle
    file_mock.__exit__.return_value = False
    return file_mock


def open_router(files):
    def _open(path, *args, **kwargs):
        return files[path]
    return _open


class TestC01111_removablemount(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01111_removablemount.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.Display')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.logger')
    def test_removable_without_nodev_noexec_warning(self, mock_logger, mock_Display, mock_InsertSection,
                                                    mock_open, mock_exists):
        mounts = make_file('/dev/sdb1 /media/usb vfat rw,suid,dev,exec 0 0\n')
        removable = make_file('1\n')
        result = make_file('')
        mock_open.side_effect = open_router({
            '/proc/mounts': mounts,
            '/sys/block/sdb1/removable': removable,
            'check_result.relt': result,
        })
        mock_exists.side_effect = lambda path: path == '/sys/block/sdb1/removable'
        C01111_module.RESULT_FILE = 'check_result.relt'

        C01111_removablemount()

        mock_InsertSection.assert_called_once_with(
            "Check whether the removable device partitions are mounted with nodev and noexec options")
        mock_open.assert_any_call('check_result.relt', 'a', encoding='utf-8')
        result.__enter__.return_value.write.assert_called_once_with('\nC01111\n')
        mock_logger.warning.assert_any_call('WRN_C01111: %s', WRN_C01111)
        mock_logger.warning.assert_any_call('SUG_C01111: %s', SUG_C01111)
        mock_Display.assert_called_once_with(
            "- The removable device partition /media/usb is not mounted with nodev and noexec options...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01111_removablemount.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.Display')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.logger')
    def test_removable_with_nodev_noexec_ok(self, mock_logger, mock_Display, mock_InsertSection,
                                            mock_open, mock_exists):
        mounts = make_file('/dev/sdb1 /media/usb vfat rw,nodev,noexec 0 0\n')
        removable = make_file('1\n')
        mock_open.side_effect = open_router({
            '/proc/mounts': mounts,
            '/sys/block/sdb1/removable': removable,
        })
        mock_exists.side_effect = lambda path: path == '/sys/block/sdb1/removable'
        C01111_module.RESULT_FILE = 'check_result.relt'

        C01111_removablemount()

        mock_InsertSection.assert_called_once_with(
            "Check whether the removable device partitions are mounted with nodev and noexec options")
        mock_logger.info.assert_called_once_with(
            "All the removable device partitions are mounted with nodev and noexec options, checking ok")
        mock_Display.assert_called_once_with(
            "- Check whether the removable device partitions are mounted with nodev and noexec options...", "OK")

    @patch('secScanner.enhance.euler.check.C01111_removablemount.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.Display')
    @patch('secScanner.enhance.euler.check.C01111_removablemount.logger')
    def test_non_removable_device_ignored(self, mock_logger, mock_Display, mock_InsertSection,
                                          mock_open, mock_exists):
        """边界：removable 内容为 0 表示非可移动设备，即使缺少 nodev/noexec 也不应告警"""
        mounts = make_file('/dev/sda1 /data ext4 rw,suid,dev,exec 0 0\n')
        removable = make_file('0\n')
        mock_open.side_effect = open_router({
            '/proc/mounts': mounts,
            '/sys/block/sda1/removable': removable,
        })
        mock_exists.side_effect = lambda path: path == '/sys/block/sda1/removable'
        C01111_module.RESULT_FILE = 'check_result.relt'

        C01111_removablemount()

        open_paths = [call.args[0] for call in mock_open.call_args_list]
        self.assertEqual(open_paths, ['/proc/mounts', '/sys/block/sda1/removable'])
        self.assertEqual(mock_exists.call_count, 1)
        mock_Display.assert_called_once_with(
            "- Check whether the removable device partitions are mounted with nodev and noexec options...", "OK")


if __name__ == '__main__':
    unittest.main()
