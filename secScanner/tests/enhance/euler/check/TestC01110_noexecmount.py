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
from unittest.mock import patch, mock_open
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01110_noexecmount import C01110_noexecmount  # Mock test setup.

class TestC01110_noexecmount(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.seconf')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_partition_not_mounted_noexec(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_seconf, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_seconf.get.return_value = '/data'
        mock_getstatusoutput.return_value = (1, '')

        # Mock test setup.
        secScanner.enhance.euler.check.C01110_noexecmount.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the partitions are mounted with noexec option")
        mock_seconf.get.assert_called_once_with('euler', 'noexecmount_points')
        mock_getstatusoutput.assert_called_once_with('mount | grep "/data" | grep "noexec"')
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01110\n")
        mock_logger.warning.assert_any_call("The partition %s is not mounted with noexec option", '/data')
        mock_logger.warning.assert_any_call("WRN_C01110: %s", WRN_C01110)
        mock_logger.warning.assert_any_call("SUG_C01110: %s", SUG_C01110)
        mock_Display.assert_called_once_with("- Check whether /data is mounted with noexec option...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.seconf')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_partition_mounted_noexec(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_seconf, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_seconf.get.return_value = '/data'
        mock_getstatusoutput.return_value = (0, '/dev/sdb1 on /data type ext4 (rw,noexec)')

        # Mock test setup.
        C01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the partitions are mounted with noexec option")
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The partition %s is mounted with noexec option, checking ok", '/data')
        mock_Display.assert_called_once_with("- Check whether /data is mounted with noexec option...", "OK")

    @patch('secScanner.enhance.euler.check.C01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.seconf')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_noexecmount_point_configured(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_seconf, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf.options.return_value = []

        # Mock test setup.
        C01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the partitions are mounted with noexec option")
        mock_seconf.get.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("No noexecmount point configured in the config file")
        mock_Display.assert_called_once_with("- No noexecmount point configured in the config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.check.C01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.seconf')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_configured_point_but_empty_value(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_seconf, mock_getstatusoutput):
        """边界：配置项存在但值为空，应视为未配置并跳过"""
        # Mock test setup.
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_seconf.get.return_value = '   '

        # Mock test setup.
        C01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the partitions are mounted with noexec option")
        mock_getstatusoutput.assert_not_called()
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with("- No noexecmount point configured in the config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.check.C01110_noexecmount.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.seconf')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.InsertSection')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.Display')
    @patch('secScanner.enhance.euler.check.C01110_noexecmount.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_partitions_mixed_result(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_seconf, mock_getstatusoutput):
        """边界：多个挂载点部分合规，只要有一个不合规即 WARNING 并写入结果文件"""
        # Mock test setup.
        mock_seconf.options.return_value = ['noexecmount_points']
        mock_seconf.get.return_value = '/data /backup'

        def fake_getstatusoutput(cmd):
            if '/backup' in cmd:
                return (1, '')
            return (0, '/dev/sdb1 on /data type ext4 (rw,noexec)')

        mock_getstatusoutput.side_effect = fake_getstatusoutput

        # Mock test setup.
        secScanner.enhance.euler.check.C01110_noexecmount.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01110_noexecmount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the partitions are mounted with noexec option")
        self.assertEqual(mock_getstatusoutput.call_count, 2)
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01110\n")
        mock_Display.assert_any_call("- Check whether /data is mounted with noexec option...", "OK")
        mock_Display.assert_any_call("- Check whether /backup is mounted with noexec option...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C01110: %s", WRN_C01110)

if __name__ == '__main__':
    unittest.main()
