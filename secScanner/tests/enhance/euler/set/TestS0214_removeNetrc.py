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
from secScanner.enhance.euler.set.S0214_removeNetrc import S0214_removeNetrc
import secScanner

class TestS0214_removeNetrc(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    def test_seconf_get_no(self, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_display.assert_called_once_with("- Skip Remove the .netrc file from the home directory due to config file...", "SKIPPING")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    def test_passwd_file_not_exists(self, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = False
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_logger.warning.assert_called_once_with("file /etc/passwd does not exist")
        mock_display.assert_called_once_with("- file /etc/passwd not exists...", "SKIPPING")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    def test_fail_obtain_user_home_list(self, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = True
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, "")
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_logger.warning.assert_called_once_with("Failed to obtain passwd user's home list")
        mock_display.assert_called_once_with("- Failed to obtain passwd user's home list ...", "FAILED")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_without_netrc_file(self, mock_isdir, mock_walk, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        # Mock test setup.
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], []), ("/home/user2", [], [])]
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_logger.info.assert_called_once_with("The .netrc file does not exist in the /home directory")
        mock_display.assert_called_once_with("- The .netrc file does not exist in the /home directory...", "SKIPPING")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.remove')
    def test_with_netrc_file_and_del_success(self, mock_remove, mock_isdir, mock_walk, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        # Mock test setup.
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], [".netrc"]), ("/home/user2", [], [])]
        # Mock test setup.
        mock_remove.return_value = None
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_logger.info.assert_any_call("Successfully deleted file /home/user1/.netrc")
        mock_display.assert_any_call("- Successfully deleted file /home/user1/.netrc", "FINISHED")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.remove')
    def test_with_netrc_file_and_del_fail(self, mock_remove, mock_isdir, mock_walk, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        # Mock test setup.
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], [".netrc"]), ("/home/user2", [], [])]
        file_path = "/home/user1/.netrc"
        # Mock test setup.
        mock_remove.side_effect = FileNotFoundError
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_logger.warning.assert_any_call(f"File {file_path} does not exist")
        mock_display.assert_any_call(f"- File {file_path} does not exist", "FAILED")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.logger')
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.set.S0214_removeNetrc.seconf.get')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.remove')
    def test_with_netrc_file_and_del_fail_os(self, mock_remove, mock_isdir, mock_walk, mock_seconf_get, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        # Mock test setup.
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        # Mock test setup.
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], [".netrc"]), ("/home/user2", [], [])]
        # mock OSError
        error = OSError()
        error.strerror = "Permission denied"
        mock_remove.side_effect = error
        # Mock test setup.
        S0214_removeNetrc()
        mock_InsertSection.assert_called_once_with("Remove the .netrc file from the home directory")
        mock_logger.warning.assert_any_call("Error deleting file /home/user1/.netrc: Permission denied")
        mock_display.assert_any_call("- Error deleting file /home/user1/.netrc: Permission denied", "FAILED")
        
if __name__ == '__main__':
    unittest.main()