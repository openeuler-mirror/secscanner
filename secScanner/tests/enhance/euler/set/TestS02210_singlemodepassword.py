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
from secScanner.enhance.euler.set.S02210_singlemodepassword import S02210_singlemodepassword  # Mock test setup.

RESCUE_SERVICE = '/usr/lib/systemd/system/rescue.service'
EMERGENCY_SERVICE = '/usr/lib/systemd/system/emergency.service'

class TestS02210_singlemodepassword(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.logger')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02210_singlemodepassword()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_singlemodepassword')
        mock_InsertSection.assert_called_once_with("set single user mode password protection...")
        mock_exists.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set single user mode password protection...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.logger')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_sulogin_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_getstatusoutput, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = lambda path: not path.endswith('_bak')
        mock_file.return_value.readlines.side_effect = [
            ['[Unit]\n', 'ExecStart=/bin/bash\n'],
            ['[Unit]\n', 'ExecStart=/bin/bash\n'],
            ['[Unit]\n', 'ExecStart=/bin/bash\n'],
            ['[Unit]\n', 'ExecStart=/bin/bash\n'],
            ['[Unit]\n', 'ExecStart=-/usr/lib/systemd/systemd-sulogin-shell rescue\n'],
            ['[Unit]\n', 'ExecStart=-/usr/lib/systemd/systemd-sulogin-shell emergency\n'],
        ]
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S02210_singlemodepassword()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_singlemodepassword')
        mock_InsertSection.assert_called_once_with("set single user mode password protection...")
        mock_getstatusoutput.assert_called_once_with('systemctl daemon-reload')
        self.assertEqual(mock_copy2.call_count, 2)
        mock_copy2.assert_any_call(RESCUE_SERVICE, RESCUE_SERVICE + '_bak')
        mock_copy2.assert_any_call(EMERGENCY_SERVICE, EMERGENCY_SERVICE + '_bak')
        mock_add_bak_file.assert_any_call(RESCUE_SERVICE + '_bak')
        mock_add_bak_file.assert_any_call(EMERGENCY_SERVICE + '_bak')
        mock_Display.assert_called_once_with("- Set single user mode password protection...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.logger')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data='[Unit]\nExecStart=/bin/bash\n')
    def test_set_sulogin_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                mock_getstatusoutput, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = lambda path: not path.endswith('_bak')
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S02210_singlemodepassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("set single user mode password protection...")
        mock_logger.warning.assert_called_once_with("set single user mode password protection failed")
        mock_Display.assert_called_once_with("- Set single user mode password protection...", "FAILED")

    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.logger')
    @patch('secScanner.enhance.euler.set.S02210_singlemodepassword.seconf.get')
    @patch('builtins.open', new_callable=mock_open,
           read_data='[Unit]\nExecStart=-/usr/lib/systemd/systemd-sulogin-shell rescue\n')
    def test_already_set_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_getstatusoutput, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：两个 service 均已使用 systemd-sulogin-shell，应跳过不修改文件"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S02210_singlemodepassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("set single user mode password protection...")
        mock_getstatusoutput.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_logger.info.assert_called_once_with("single user mode password protection is already set")
        mock_Display.assert_called_once_with("- Already set single user mode password protection...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
