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
from secScanner.enhance.euler.set.S01107_filesystemmod import S01107_filesystemmod  # Mock test setup.

FILESYSTEMS = ["cramfs", "freevxfs", "jffs2", "hfs", "hfsplus", "squashfs", "udf", "vfat",
               "fat", "msdos", "nfs", "ceph", "fuse", "overlay", "xfs"]
MODPROBE_CONF = '/etc/modprobe.d/secscanner.conf'
CONF_TEXT = "".join("install %s /bin/true\n" % fs for fs in FILESYSTEMS)

def _exists(path, modprobe_d=True, conf=True, bak=False):
    if path == '/etc/modprobe.d':
        return modprobe_d
    if path == MODPROBE_CONF:
        return conf
    if path == MODPROBE_CONF + '_bak':
        return bak
    return False

def _getstatusoutput(loaded):
    def fake(cmd):
        if cmd.startswith('lsmod'):
            return (0, 'cramfs 1 0') if loaded else (1, '')
        return (1, '')
    return fake

class TestS01107_filesystemmod(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chmod')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chown', create=True)
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.makedirs')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.logger')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak, mock_getstatusoutput, mock_run, mock_makedirs, mock_chown, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01107_filesystemmod()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_filesystemmod')
        mock_InsertSection.assert_called_once_with("Ban the unneeded filesystems from being mounted...")
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with("- Skip ban the unneeded filesystems...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chmod')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chown', create=True)
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.makedirs')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.logger')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data=CONF_TEXT)
    def test_ban_filesystems_success_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak, mock_getstatusoutput, mock_run, mock_makedirs, mock_chown, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists
        mock_getstatusoutput.side_effect = _getstatusoutput(False)

        # Mock test setup.
        S01107_filesystemmod()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Ban the unneeded filesystems from being mounted...")
        mock_makedirs.assert_not_called()
        mock_copy2.assert_called_once_with(MODPROBE_CONF, MODPROBE_CONF + '_bak')
        mock_add_bak.assert_called_once_with(MODPROBE_CONF + '_bak')
        mock_file.assert_any_call(MODPROBE_CONF, 'a')
        mock_file.assert_any_call(MODPROBE_CONF, 'r')
        mock_file().write.assert_any_call("install cramfs /bin/true\n")
        self.assertEqual(mock_file().write.call_count, len(FILESYSTEMS))
        mock_run.assert_not_called()
        mock_chown.assert_called_once_with(MODPROBE_CONF, 0, 0)
        mock_chmod.assert_called_once_with(MODPROBE_CONF, 0o600)
        mock_logger.info.assert_any_call("Ban the unneeded filesystems finished, checking ok")
        mock_Display.assert_called_once_with("- Ban the unneeded filesystems from being mounted...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chmod')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chown', create=True)
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.makedirs')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.logger')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_conf_verify_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak, mock_getstatusoutput, mock_run, mock_makedirs, mock_chown, mock_chmod):
        """边界：写入后回读配置不含 install 规则，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists
        mock_getstatusoutput.side_effect = _getstatusoutput(False)

        # Mock test setup.
        S01107_filesystemmod()

        # Mock test setup.
        self.assertEqual(mock_file().write.call_count, len(FILESYSTEMS))
        mock_logger.warning.assert_called_once_with("Ban the unneeded filesystems failed")
        mock_Display.assert_called_once_with("- Ban the unneeded filesystems from being mounted...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chmod')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chown', create=True)
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.makedirs')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.logger')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data=CONF_TEXT)
    def test_remove_filesystem_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak, mock_getstatusoutput, mock_run, mock_makedirs, mock_chown, mock_chmod):
        """边界：已加载模块卸载失败，配置虽完整仍应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists
        mock_getstatusoutput.side_effect = _getstatusoutput(True)
        mock_run.return_value.returncode = 1

        # Mock test setup.
        S01107_filesystemmod()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, len(FILESYSTEMS))
        mock_run.assert_any_call(['modprobe', '-r', 'cramfs'], capture_output=True)
        mock_logger.warning.assert_any_call("Remove the %s filesystem failed", 'cramfs')
        mock_Display.assert_called_once_with("- Ban the unneeded filesystems from being mounted...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chmod')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.chown', create=True)
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.makedirs')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.logger')
    @patch('secScanner.enhance.euler.set.S01107_filesystemmod.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data=CONF_TEXT)
    def test_modprobe_dir_and_conf_missing_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak, mock_getstatusoutput, mock_run, mock_makedirs, mock_chown, mock_chmod):
        """边界：/etc/modprobe.d 与配置文件均不存在，应创建目录且不备份"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = lambda path: _exists(path, modprobe_d=False, conf=False)
        mock_getstatusoutput.side_effect = _getstatusoutput(False)

        # Mock test setup.
        S01107_filesystemmod()

        # Mock test setup.
        mock_makedirs.assert_called_once_with('/etc/modprobe.d')
        mock_copy2.assert_not_called()
        mock_add_bak.assert_not_called()
        self.assertEqual(mock_file().write.call_count, len(FILESYSTEMS))
        mock_Display.assert_called_once_with("- Ban the unneeded filesystems from being mounted...", "FINISHED")

if __name__ == '__main__':
    unittest.main()
