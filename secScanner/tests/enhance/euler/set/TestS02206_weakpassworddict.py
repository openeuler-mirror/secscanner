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
from secScanner.enhance.euler.set.S02206_weakpassworddict import S02206_weakpassworddict


def _make_open(files, opened, writable=True):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(files.get(path, []))
        elif "a" in mode:
            files.setdefault(path, [])
            if writable:
                handle.write.side_effect = lambda data: files[path].append(data)
        elif "w" in mode:
            if writable:
                files[path] = []
                handle.writelines.side_effect = lambda lines: files.__setitem__(path, list(lines))
                handle.write.side_effect = lambda data: files[path].append(data)
        return handle
    return _open


def _make_exists(files):
    def _exists(path):
        if path.endswith("_bak"):
            return False
        return path in files
    return _exists


class TestS02206_weakpassworddict(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.seconf.get')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.InsertSection')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.logger')
    def test_config_disabled_skipping(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02206_weakpassworddict()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_weakpassworddict')
        mock_InsertSection.assert_called_once_with("set that the weak password dictionary is set correctly...")
        mock_Display.assert_called_once_with("- Skip set the weak password dictionary...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.seconf.get')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.InsertSection')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.logger')
    def test_already_set_skipping(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get, mock_exists):
        """边界：弱口令字典配置已正确时应跳过"""
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_pwquality.so try_first_pass local_users_only\n'],
            '/etc/security/pwquality.conf': ['minlen = 8\n'],
            '/usr/share/cracklib/pw_dict.hwm': [],
        }
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists(files)
        opened = []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, opened)):
            S02206_weakpassworddict()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_weakpassworddict')
        mock_InsertSection.assert_called_once_with("set that the weak password dictionary is set correctly...")
        mock_logger.info.assert_called_once_with("weak password dictionary is already set correctly")
        mock_Display.assert_called_once_with("- Already set the weak password dictionary correctly...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.remove')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.path.getsize')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.seconf.get')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.InsertSection')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.logger')
    def test_set_weak_password_dict_finished(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get,
                                             mock_exists, mock_copy2, mock_add_bak_file, mock_getstatusoutput,
                                             mock_getsize, mock_remove):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_pwquality.so try_first_pass local_users_only enforce_for_root dictcheck=0\n'],
            '/etc/security/pwquality.conf': ['dictcheck = 0\n'],
            '/usr/share/cracklib/pw_dict.hwm': [],
            '/var/tmp/dictionary.txt': [],
        }
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists(files)
        mock_getsize.return_value = 1024
        mock_getstatusoutput.side_effect = [(0, ''), (0, '')]
        opened = []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, opened)):
            S02206_weakpassworddict()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_weakpassworddict')
        mock_InsertSection.assert_called_once_with("set that the weak password dictionary is set correctly...")
        self.assertEqual(mock_copy2.call_count, 2)
        mock_add_bak_file.assert_any_call('/etc/pam.d/system-auth_bak')
        mock_add_bak_file.assert_any_call('/etc/security/pwquality.conf_bak')
        self.assertEqual(mock_getstatusoutput.call_count, 2)
        mock_getstatusoutput.assert_any_call('cracklib-unpacker /usr/share/cracklib/pw_dict > /var/tmp/dictionary.txt')
        mock_getstatusoutput.assert_any_call('create-cracklib-dict /var/tmp/dictionary.txt')
        mock_remove.assert_called_once_with('/var/tmp/dictionary.txt')
        mock_logger.info.assert_any_call("update the weak password dictionary successfully")
        mock_logger.info.assert_any_call("set the weak password dictionary successfully")
        mock_Display.assert_called_once_with("- Set the weak password dictionary correctly...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.remove')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.path.getsize')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.seconf.get')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.InsertSection')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.set.S02206_weakpassworddict.logger')
    def test_set_weak_password_dict_failed(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get,
                                           mock_exists, mock_copy2, mock_add_bak_file, mock_getstatusoutput,
                                           mock_getsize, mock_remove):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_pwquality.so try_first_pass local_users_only enforce_for_root dictcheck=0\n'],
            '/etc/security/pwquality.conf': ['dictcheck = 0\n'],
            '/usr/share/cracklib/pw_dict.hwm': [],
        }
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists(files)
        mock_getstatusoutput.return_value = (1, 'unpack failed')
        opened = []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, opened, writable=False)):
            S02206_weakpassworddict()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("set that the weak password dictionary is set correctly...")
        mock_logger.warning.assert_any_call("unpack the weak password dictionary failed: unpack failed")
        mock_logger.warning.assert_called_with("set the weak password dictionary failed")
        mock_Display.assert_called_once_with("- Set the weak password dictionary correctly...", "FAILED")

if __name__ == '__main__':
    unittest.main()
