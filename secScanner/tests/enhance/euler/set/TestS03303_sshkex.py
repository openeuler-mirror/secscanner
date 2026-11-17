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
from secScanner.enhance.euler.set.S03303_sshkex import S03303_sshkex


KEX_VALUE = "curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256"


class TestS03303_sshkex(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.Display')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.logger')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03303_sshkex()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sshkex')
        mock_InsertSection.assert_called_once_with("Set config of KexAlgorithms...")
        mock_Display.assert_called_once_with("Skip set KexAlgorithms due to config file...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_add_bak_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.Display')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.logger')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="KexAlgorithms " + KEX_VALUE + "\n")
    def test_already_set_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', KEX_VALUE]
        mock_exists.return_value = True

        # Mock test setup.
        S03303_sshkex()

        # Mock test setup.
        mock_seconf_get.assert_any_call('euler', 'set_sshkex')
        mock_seconf_get.assert_any_call('euler', 'ssh_kexalgorithms_value')
        mock_InsertSection.assert_called_once_with("Set config of KexAlgorithms...")
        mock_add_bak_file.assert_called_once_with('/etc/ssh/sshd_config_bak')
        mock_copy2.assert_not_called()
        mock_logger.info.assert_called_once_with("Check set of KexAlgorithms right")
        mock_Display.assert_called_once_with("- Already right set KexAlgorithms in sshd config", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.Display')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.logger')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_and_verify_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                       mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', KEX_VALUE]
        mock_exists.return_value = True
        bad_read = mock_open(read_data="KexAlgorithms diffie-hellman-group14-sha1\n")()
        write_handle = mock_open()()
        verify_read = mock_open(read_data="KexAlgorithms " + KEX_VALUE + "\n")()
        mock_file.side_effect = [bad_read, write_handle, verify_read]

        # Mock test setup.
        S03303_sshkex()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set config of KexAlgorithms...")
        mock_file.assert_any_call("/etc/ssh/sshd_config", "w")
        write_handle.write.assert_any_call("KexAlgorithms " + KEX_VALUE + "\n")
        mock_logger.info.assert_any_call("Set KexAlgorithms finish")
        mock_Display.assert_called_once_with("- Set KexAlgorithms in sshd config and restart sshd service", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.Display')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.logger')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_after_write_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                       mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', KEX_VALUE]
        mock_exists.return_value = True
        bad_read = mock_open(read_data="KexAlgorithms diffie-hellman-group14-sha1\n")()
        write_handle = mock_open()()
        verify_read = mock_open(read_data="KexAlgorithms diffie-hellman-group14-sha1\n")()
        mock_file.side_effect = [bad_read, write_handle, verify_read]

        # Mock test setup.
        S03303_sshkex()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set config of KexAlgorithms...")
        mock_logger.warning.assert_called_once_with("Set KexAlgorithms failed")
        mock_Display.assert_called_once_with("- Set KexAlgorithms in sshd config", "FAILED")

    @patch('secScanner.enhance.euler.set.S03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.Display')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.logger')
    @patch('secScanner.enhance.euler.set.S03303_sshkex.seconf.get')
    def test_config_file_not_exist_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                          mock_add_bak_file, mock_copy2, mock_exists):
        """边界：sshd 配置文件不存在时应 FAILED"""
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', KEX_VALUE]
        mock_exists.return_value = False

        # Mock test setup.
        S03303_sshkex()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set config of KexAlgorithms...")
        mock_add_bak_file.assert_not_called()
        mock_logger.warning.assert_called_once_with("sshd config file not exist")
        mock_Display.assert_called_once_with("- sshd config file not exist", "FAILED")


if __name__ == '__main__':
    unittest.main()
