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
from secScanner.enhance.euler.set.S01111_removablemount import S01111_removablemount


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


class TestS01111_removablemount(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01111_removablemount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.Display')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.logger')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_getstatusoutput):
        mock_seconf_get.return_value = 'no'

        S01111_removablemount()

        mock_seconf_get.assert_called_once_with('euler', 'set_removablemount')
        mock_InsertSection.assert_called_once_with(
            "Remount the removable device partitions with nodev and noexec options...")
        mock_Display.assert_called_once_with("- Skip remount the removable device partitions...", "SKIPPING")
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S01111_removablemount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.subprocess.getstatusoutput')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.Display')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.logger')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.seconf.get')
    def test_remount_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_open, mock_getstatusoutput, mock_exists):
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '')
        mock_open.side_effect = open_router({
            '/proc/mounts': make_file('/dev/sdb1 /media/usb vfat rw,suid,dev,exec 0 0\n'),
            '/sys/block/sdb1/removable': make_file('1\n'),
        })
        mock_exists.side_effect = lambda path: path == '/sys/block/sdb1/removable'

        S01111_removablemount()

        mock_seconf_get.assert_called_once_with('euler', 'set_removablemount')
        mock_getstatusoutput.assert_called_once_with('mount -o remount,nodev,noexec "/media/usb"')
        mock_Display.assert_called_once_with(
            "- Remount the removable device partitions with nodev and noexec options...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01111_removablemount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.subprocess.getstatusoutput')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.Display')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.logger')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.seconf.get')
    def test_remount_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                            mock_open, mock_getstatusoutput, mock_exists):
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (1, 'mount: failed')
        mock_open.side_effect = open_router({
            '/proc/mounts': make_file('/dev/sdb1 /media/usb vfat rw,suid,dev,exec 0 0\n'),
            '/sys/block/sdb1/removable': make_file('1\n'),
        })
        mock_exists.side_effect = lambda path: path == '/sys/block/sdb1/removable'

        S01111_removablemount()

        mock_getstatusoutput.assert_called_once_with('mount -o remount,nodev,noexec "/media/usb"')
        mock_logger.warning.assert_any_call(
            "Remount the removable device partition %s failed: %s", '/media/usb', 'mount: failed')
        mock_Display.assert_called_once_with(
            "- Remount the removable device partitions with nodev and noexec options...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01111_removablemount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.subprocess.getstatusoutput')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.Display')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.logger')
    @patch('secScanner.enhance.euler.set.S01111_removablemount.seconf.get')
    def test_no_bad_mounts_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                    mock_open, mock_getstatusoutput, mock_exists):
        """边界：可移动设备已带 nodev/noexec 时无需重挂载，应输出 SKIPPING"""
        mock_seconf_get.return_value = 'yes'
        mock_open.side_effect = open_router({
            '/proc/mounts': make_file('/dev/sdb1 /media/usb vfat rw,nodev,noexec 0 0\n'),
            '/sys/block/sdb1/removable': make_file('1\n'),
        })
        mock_exists.side_effect = lambda path: path == '/sys/block/sdb1/removable'

        S01111_removablemount()

        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with(
            "- All the removable device partitions are already mounted with nodev and noexec options...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()
