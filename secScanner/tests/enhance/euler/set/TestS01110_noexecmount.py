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
import logging
from secScanner.enhance.euler.set.S01110_noexecmount import S01110_noexecmount  # Mock test setup.

class TestS01110_noexecmount(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.logger')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.seconf')
    def test_config_disabled_skipping(self, mock_seconf, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf.get.return_value = 'no'

        # Mock test setup.
        S01110_noexecmount()

        # Mock test setup.
        mock_seconf.get.assert_called_once_with('euler', 'set_noexecmount')
        mock_InsertSection.assert_called_once_with("Remount the partitions with noexec option...")
        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with("- Skip remount the partitions with noexec option...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.logger')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.seconf')
    def test_remount_all_success_finished(self, mock_seconf, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        def fake_seconf_get(section, key):
            return {'set_noexecmount': 'yes', 'noexecmount_points': '/data /backup'}[key]

        mock_seconf.get.side_effect = fake_seconf_get
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_getstatusoutput.side_effect = [(1, ''), (0, ''), (1, ''), (0, '')]

        # Mock test setup.
        S01110_noexecmount()

        # Mock test setup.
        mock_seconf.get.assert_any_call('euler', 'set_noexecmount')
        mock_InsertSection.assert_called_once_with("Remount the partitions with noexec option...")
        self.assertEqual(mock_getstatusoutput.call_count, 4)
        mock_getstatusoutput.assert_any_call('mount | grep "/data" | grep "noexec"')
        mock_getstatusoutput.assert_any_call('mount -o remount,noexec "/data"')
        mock_getstatusoutput.assert_any_call('mount | grep "/backup" | grep "noexec"')
        mock_getstatusoutput.assert_any_call('mount -o remount,noexec "/backup"')
        mock_logger.info.assert_any_call("Remount the partition %s with noexec option finished", '/data')
        mock_Display.assert_called_once_with("- Remount the partitions with noexec option...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.logger')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.seconf')
    def test_remount_failed(self, mock_seconf, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        def fake_seconf_get(section, key):
            return {'set_noexecmount': 'yes', 'noexecmount_points': '/data'}[key]

        mock_seconf.get.side_effect = fake_seconf_get
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_getstatusoutput.side_effect = [(1, ''), (1, 'remount: failed')]

        # Mock test setup.
        S01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remount the partitions with noexec option...")
        mock_logger.warning.assert_any_call("Remount the partition %s with noexec option failed: %s", '/data', 'remount: failed')
        mock_logger.warning.assert_any_call("Remount the partitions with noexec option failed")
        mock_Display.assert_called_once_with("- Remount the partitions with noexec option...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.logger')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.seconf')
    def test_no_noexecmount_point_configured(self, mock_seconf, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：未配置 noexecmount_points，应跳过且不执行 mount"""
        # Mock test setup.
        mock_seconf.get.return_value = 'yes'
        mock_seconf.options.return_value = []

        # Mock test setup.
        S01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remount the partitions with noexec option...")
        mock_getstatusoutput.assert_not_called()
        mock_logger.info.assert_called_once_with("No noexecmount point configured in the config file")
        mock_Display.assert_called_once_with("- No noexecmount point configured in the config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.logger')
    @patch('secScanner.enhance.euler.set.S01110_noexecmount.seconf')
    def test_already_mounted_noexec_skipping(self, mock_seconf, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：挂载点已带 noexec，无需重挂，应跳过"""
        # Mock test setup.
        def fake_seconf_get(section, key):
            return {'set_noexecmount': 'yes', 'noexecmount_points': '/data'}[key]

        mock_seconf.get.side_effect = fake_seconf_get
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_getstatusoutput.return_value = (0, '/dev/sdb1 on /data type ext4 (rw,noexec)')

        # Mock test setup.
        S01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remount the partitions with noexec option...")
        mock_getstatusoutput.assert_called_once_with('mount | grep "/data" | grep "noexec"')
        mock_logger.info.assert_any_call("The partition %s has already been mounted with noexec option", '/data')
        mock_Display.assert_called_once_with("- All the partitions are already mounted with noexec option...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
