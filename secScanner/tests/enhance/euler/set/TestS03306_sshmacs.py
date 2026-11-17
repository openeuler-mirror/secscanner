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
from secScanner.enhance.euler.set.S03306_sshmacs import S03306_sshmacs


MAC_VALUE = "hmac-sha2-512,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-256-etm@openssh.com"


class TestS03306_sshmacs(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.logger')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03306_sshmacs()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sshmacs')
        mock_InsertSection.assert_called_once_with("Set config of MACs...")
        mock_Display.assert_called_once_with("Skip set MACs due to config file...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_add_bak_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.logger')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="MACs " + MAC_VALUE + "\n")
    def test_already_set_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', MAC_VALUE]
        mock_exists.return_value = True

        # Mock test setup.
        S03306_sshmacs()

        # Mock test setup.
        mock_seconf_get.assert_any_call('euler', 'set_sshmacs')
        mock_seconf_get.assert_any_call('euler', 'ssh_macs_value')
        mock_InsertSection.assert_called_once_with("Set config of MACs...")
        mock_add_bak_file.assert_called_once_with('/etc/ssh/sshd_config_bak')
        mock_copy2.assert_not_called()
        mock_logger.info.assert_called_once_with("Check set of MACs right")
        mock_Display.assert_called_once_with("- Already right set MACs in sshd config", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.logger')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_and_verify_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                       mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', MAC_VALUE]
        mock_exists.return_value = True
        bad_read = mock_open(read_data="MACs hmac-md5,hmac-sha1\n")()
        write_handle = mock_open()()
        verify_read = mock_open(read_data="MACs " + MAC_VALUE + "\n")()
        mock_file.side_effect = [bad_read, write_handle, verify_read]

        # Mock test setup.
        S03306_sshmacs()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set config of MACs...")
        mock_file.assert_any_call("/etc/ssh/sshd_config", "w")
        write_handle.write.assert_any_call("MACs " + MAC_VALUE + "\n")
        mock_logger.info.assert_any_call("Set MACs finish")
        mock_Display.assert_called_once_with("- Set MACs in sshd config and restart sshd service", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.logger')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_after_write_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                       mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', MAC_VALUE]
        mock_exists.return_value = True
        bad_read = mock_open(read_data="MACs hmac-md5,hmac-sha1\n")()
        write_handle = mock_open()()
        verify_read = mock_open(read_data="MACs hmac-md5,hmac-sha1\n")()
        mock_file.side_effect = [bad_read, write_handle, verify_read]

        # Mock test setup.
        S03306_sshmacs()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set config of MACs...")
        mock_logger.warning.assert_called_once_with("Set MACs failed")
        mock_Display.assert_called_once_with("- Set MACs in sshd config", "FAILED")

    @patch('secScanner.enhance.euler.set.S03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.logger')
    @patch('secScanner.enhance.euler.set.S03306_sshmacs.seconf.get')
    def test_config_file_not_exist_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                          mock_add_bak_file, mock_copy2, mock_exists):
        """边界：sshd 配置文件不存在时应 FAILED"""
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', MAC_VALUE]
        mock_exists.return_value = False

        # Mock test setup.
        S03306_sshmacs()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set config of MACs...")
        mock_add_bak_file.assert_not_called()
        mock_logger.warning.assert_called_once_with("sshd config file not exist")
        mock_Display.assert_called_once_with("- sshd config file not exist", "FAILED")


if __name__ == '__main__':
    unittest.main()
