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
from unittest.mock import patch, mock_open, call
import os
import sys
import secScanner
from secScanner.enhance.euler.set.S0206_accountToHome import S0206_accountToHome

class TestS0206_accountToHome(unittest.TestCase):
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.InsertSection')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.seconf.get')
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.add_bak_file')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.Display')
    def test_account_to_home_disabled(self, mock_display, mock_logger, mock_getstatusoutput, mock_add_bak_file, mock_copy2, mock_os_path_exists, mock_seconf_get, mock_InsertSection):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S0206_accountToHome()
        mock_InsertSection.assert_any_call("Confirm that the account has its own home directory")
        mock_display.assert_any_call("- Skip confirm if the account has its own home directory due to config file...", "SKIPPING")
    
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.InsertSection')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.seconf.get')
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.add_bak_file')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.Display')
    def test_passwd_file_not_exist(self, mock_display, mock_logger, mock_getstatusoutput, mock_add_bak_file, mock_copy2, mock_os_path_exists, mock_seconf_get, mock_InsertSection):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_os_path_exists.return_value = False

        # Mock test setup.
        S0206_accountToHome()
        mock_InsertSection.assert_called_once_with("Confirm that the account has its own home directory")
        mock_logger.warning.assert_called_once_with("file /etc/passwd does not exist")
        mock_display.assert_called_once_with("- file /etc/passwd not exists...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S0206_accountToHome.InsertSection')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.seconf.get')
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.add_bak_file')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.Display')
    def test_fail_obtain_passwd_user_list(self, mock_display, mock_logger, mock_getstatusoutput, mock_add_bak_file, mock_copy2, mock_os_path_exists, mock_seconf_get, mock_InsertSection):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_os_path_exists.side_effect = [True, False, False]
        # Mock test setup.

        # Mock test setup.
        mock_getstatusoutput.side_effect = [
            (1, ''),
            (1, '')
        ]

        # Mock test setup.
        S0206_accountToHome()

        mock_InsertSection.assert_called_once_with("Confirm that the account has its own home directory")
        mock_copy2.assert_any_call('/etc/passwd', '/etc/passwd_bak')
        mock_copy2.assert_any_call('/etc/shadow', '/etc/shadow_bak')
        mock_add_bak_file.assert_any_call('/etc/passwd_bak')
        mock_add_bak_file.assert_any_call('/etc/shadow_bak')
        mock_logger.warning.assert_called_once_with("Failed to obtain passwd user list")
        mock_display.assert_called_once_with("- Failed to obtain passwd user list ...", "FAILED")

    @patch('secScanner.enhance.euler.set.S0206_accountToHome.InsertSection')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.seconf.get')
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.add_bak_file')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.Display')
    @patch('os.path.isdir')
    def test_user_have_home_directory(self, mock_isdir, mock_display, mock_logger, mock_getstatusoutput, mock_add_bak_file, mock_copy2, mock_os_path_exists, mock_seconf_get, mock_InsertSection):   
        
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_os_path_exists.return_value = True

        # Mock test setup.
        mock_getstatusoutput.side_effect = [
            (0, 'root:x:0:0:root:/root:/bin/bash\nuser1:x:1000:1000::/home/user1:/bin/bash'),
            (0, 'drwxr-xr-x. 8 root root 4096 10月 31 00:47 /root'),
            (0, 'drwxrwxrwx. 9 user1 user1 4096 10月 29 06:35 /home/user1'),
            (0, 'root:x:0:0:root:/root:/bin/bash\nuser1:x:1000:1000::/home/user1:/bin/bash'),
            (0, 'drwxr-xr-x. 8 root root 4096 10月 31 00:47 /root'),
            (0, 'drwxrwxrwx. 9 user1 user1 4096 10月 29 06:35 /home/user1'),
        ]
        # Mock test setup.
        S0206_accountToHome()

        # Mock test setup.
        mock_logger.info.assert_called_with("Confirm that the account has its own home directory")
        mock_display.assert_called_with("- Confirm that the account has its own home directory...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S0206_accountToHome.InsertSection')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.seconf.get')
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.add_bak_file')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.Display')
    @patch('os.path.isdir')
    def test_re_add_user_home_directory(self, mock_isdir, mock_display, mock_logger, mock_getstatusoutput, mock_add_bak_file, mock_copy2, mock_os_path_exists, mock_seconf_get, mock_InsertSection):   
        
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_os_path_exists.return_value = True

        mock_getstatusoutput.side_effect = [
            (0, 'root:x:0:0:root:/root:/bin/bash\nuser1:x:1000:1000::/home/user1:/bin/bash'),
            (0, 'drwxr-xr-x. 8 root root 4096 10月 31 00:47 /root'),
            (1, ''),  # Mock test setup.
            (0, ''),  # Mock test setup.
            (0, ''),  # Mock test setup.
            (0, 'root:x:0:0:root:/root:/bin/bash\nuser1:x:1000:1000::/home/user1:/bin/bash'),
            (0, 'drwxr-xr-x. 8 root root 4096 10月 31 00:47 /root'),
            (0, 'drwxrwxrwx. 9 user1 user1 4096 10月 29 06:35 /home/user1'),
        ]
        # Mock test setup.
        S0206_accountToHome()

        # Mock test setup.
        mock_logger.info.assert_called_with("Confirm that the account has its own home directory")
        mock_display.assert_called_with("- Confirm that the account has its own home directory...", "FINISHED")
    
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.InsertSection')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.seconf.get')
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.add_bak_file')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.logger')
    @patch('secScanner.enhance.euler.set.S0206_accountToHome.Display')
    @patch('os.path.isdir')
    def test_uncorrect_home_directory(self, mock_isdir, mock_display, mock_logger, mock_getstatusoutput, mock_add_bak_file, mock_copy2, mock_os_path_exists, mock_seconf_get, mock_InsertSection):   
        
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_os_path_exists.return_value = True

        # Mock test setup.
        mock_getstatusoutput.side_effect = [
            (0, 'root:x:0:0:root:/root:/bin/bash\nuser1:x:1000:1000::/home/user1:/bin/bash'),
            (0, 'drwxr-xr-x. 8 root root 4096 10月 31 00:47 /root'),
            (0, 'drwxrwxrwx. 9 user1 user1 4096 10月 29 06:35 /home/user'),
            (0, 'root:x:0:0:root:/root:/bin/bash\nuser1:x:1000:1000::/home/user1:/bin/bash'),
            (0, 'drwxr-xr-x. 8 root2 root2 4096 10月 31 00:47 /root2'),
            (0, 'drwxrwxrwx. 9 user2 user2 4096 10月 29 06:35 /home/user2')
        ]
        # Mock test setup.
        S0206_accountToHome()

        # Mock test setup.
        mock_logger.warning.assert_called_with("At least one home directory does not match the user")
        mock_display.assert_called_with("- At least one home directory does not match the user", "FAILED")
    
if __name__ == '__main__':
    unittest.main()