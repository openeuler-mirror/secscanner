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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.set.S0212_expiredAccount import S0212_expiredAccount
import secScanner

class TestS0212_expiredAccount(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open,read_data='user1:$6$hash:17597:0:99999:7:::\nuser2:$6$hash:17597:0:99999:7::17000\n')
    @patch('enhance.euler.set.S0212_expiredAccount.datetime')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.seconf.get')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.add_bak_file')
    def test_expired_account_exists_and_deluser_success(self, mock_add_bak_file, mock_copy2, mock_seconf_get, mock_datetime, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.side_effect = [True, False]
        # Mock test setup.
        mock_datetime.datetime.now.timestamp.return_value = 1730684465
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, "")
        # Mock test setup.
        S0212_expiredAccount()
        mock_InsertSection.assert_any_call("Delete expired account")
        mock_copy2.assert_any_call('/etc/shadow', '/etc/shadow_bak')
        mock_add_bak_file.assert_any_call('/etc/shadow_bak')
        mock_logger.info.assert_any_call('No expired account exists')
        mock_display.assert_called_once_with("- No expired account exists", "FINISHED")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open,read_data='user1:$6$hash:17597:0:99999:7:::\nuser2:$6$hash:17597:0:99999:7::17000\n')
    @patch('enhance.euler.set.S0212_expiredAccount.datetime')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.seconf.get')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.add_bak_file')
    def test_expired_account_exists_and_deluser_failed(self, mock_add_bak_file, mock_copy2, mock_seconf_get, mock_datetime, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.side_effect = [True, False]
        # Mock test setup.
        mock_datetime.datetime.now.timestamp.return_value = 1730684465
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, "")
        # Mock test setup.
        S0212_expiredAccount()
        mock_InsertSection.assert_any_call("Delete expired account")
        mock_copy2.assert_any_call('/etc/shadow', '/etc/shadow_bak')
        mock_add_bak_file.assert_any_call('/etc/shadow_bak')
        mock_logger.warning.assert_any_call('At least one account has expired.')
        mock_display.assert_called_once_with("- At least one account has expired", "FAILED")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open, read_data='user1:$6$hash:17597:0:99999:7:::\nuser2:$6$hash:17597:0:99999:7:::\n')
    @patch('enhance.euler.set.S0212_expiredAccount.datetime')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.seconf.get')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.add_bak_file')
    def test_no_expired_accounts(self, mock_add_bak_file, mock_copy2, mock_seconf_get, mock_datetime, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.side_effect = [True, False]
        # Mock test setup.
        mock_datetime.datetime.now.timestamp.return_value = 1730684465

        # Mock test setup.
        S0212_expiredAccount()
        mock_InsertSection.assert_any_call("Delete expired account")
        mock_copy2.assert_any_call('/etc/shadow', '/etc/shadow_bak')
        mock_add_bak_file.assert_any_call('/etc/shadow_bak')
        mock_logger.info.assert_any_call('No expired account exists')
        mock_display.assert_called_once_with("- No expired account exists", "FINISHED")


    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.seconf.get')
    def test_shadow_file_not_exists(self, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = False
        # Mock test setup.
        S0212_expiredAccount()
        mock_InsertSection.assert_any_call("Delete expired account")
        mock_logger.warning.assert_any_call("file /etc/shadow dose not exist")
        mock_display.assert_any_call("- file /etc/shadow dose not exist...", "SKIPPING")

    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0212_expiredAccount.seconf.get')
    def test_seconf_get_no(self, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'
        # Mock test setup.
        S0212_expiredAccount()
        mock_InsertSection.assert_any_call("Delete expired account")
        mock_display.assert_any_call("- Skip check for expired account due to config file...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()