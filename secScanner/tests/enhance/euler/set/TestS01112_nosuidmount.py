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
from unittest.mock import patch
from secScanner.enhance.euler.set.S01112_nosuidmount import S01112_nosuidmount

MOUNT_CMD = 'mount | grep -v "nosuid" | awk -F " " \'{print $3}\''


class TestS01112_nosuidmount(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.logger')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_getstatusoutput):
        mock_seconf_get.return_value = 'no'

        S01112_nosuidmount()

        mock_seconf_get.assert_called_once_with('euler', 'set_nosuidmount')
        mock_InsertSection.assert_called_once_with("Remount the partitions with nosuid option...")
        mock_Display.assert_called_once_with("- Skip remount the partitions with nosuid option...", "SKIPPING")
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.logger')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.seconf.get')
    def test_remount_success_finished(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_getstatusoutput):
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, '/data\n'), (0, '')]

        S01112_nosuidmount()

        mock_seconf_get.assert_called_once_with('euler', 'set_nosuidmount')
        self.assertEqual(mock_getstatusoutput.call_count, 2)
        mock_getstatusoutput.assert_any_call(MOUNT_CMD)
        mock_getstatusoutput.assert_any_call('mount -o remount,nosuid "/data"')
        mock_Display.assert_called_once_with("- Remount the partitions with nosuid option...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.logger')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.seconf.get')
    def test_remount_failed(self, mock_seconf_get, mock_logger, mock_Display,
                            mock_InsertSection, mock_getstatusoutput):
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, '/data\n'), (1, 'mount: failed')]

        S01112_nosuidmount()

        mock_logger.warning.assert_any_call(
            "Remount the partition %s with nosuid option failed: %s", '/data', 'mount: failed')
        mock_Display.assert_called_once_with("- Remount the partitions with nosuid option...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.Display')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.logger')
    @patch('secScanner.enhance.euler.set.S01112_nosuidmount.seconf.get')
    def test_empty_result_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                   mock_InsertSection, mock_getstatusoutput):
        """边界：mount 命令无输出时没有需要处理的挂载点，应输出 SKIPPING"""
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '  \n')

        S01112_nosuidmount()

        self.assertEqual(mock_getstatusoutput.call_count, 1)
        mock_Display.assert_called_once_with(
            "- All the partitions are already mounted with nosuid option...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()
