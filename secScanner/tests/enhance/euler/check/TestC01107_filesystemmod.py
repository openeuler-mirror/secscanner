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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01107_filesystemmod import C01107_filesystemmod  # Mock test setup.

class TestC01107_filesystemmod(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_filesystems_not_banned(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        def side_effect(cmd):
            if cmd.startswith('modprobe'):
                return (1, '')
            return (0, 'cramfs 1 0')

        mock_getstatusoutput.side_effect = side_effect

        # Mock test setup.
        secScanner.enhance.euler.check.C01107_filesystemmod.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01107_filesystemmod()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the unneeded filesystems are banned from being mounted")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_any_call("\nC01107\n")
        self.assertEqual(mock_file().write.call_count, 15)
        mock_logger.warning.assert_any_call("WRN_C01107_%02d: %s", 1, WRN_C01107_01)
        mock_logger.warning.assert_any_call("SUG_C01107_%02d: %s", 15, SUG_C01107_15)
        mock_Display.assert_any_call("- The cramfs filesystem is not banned from mounting...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_filesystems_banned(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, 'install /bin/true')

        # Mock test setup.
        C01107_filesystemmod()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the unneeded filesystems are banned from being mounted")
        self.assertEqual(mock_getstatusoutput.call_count, 15)
        mock_file.assert_not_called()
        mock_logger.info.assert_any_call("The %s filesystem is banned from being mounted, checking ok", 'cramfs')
        mock_Display.assert_any_call("- Check whether the xfs filesystem is banned from mounting...", "OK")

    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_filesystem_not_supported(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：模块不存在且未加载时应视为系统不支持该文件系统"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, '')

        # Mock test setup.
        C01107_filesystemmod()

        # Mock test setup.
        self.assertEqual(mock_getstatusoutput.call_count, 30)
        mock_file.assert_not_called()
        mock_logger.info.assert_any_call("The %s filesystem is not supported in the system, checking ok", 'cramfs')
        mock_Display.assert_any_call("- Check whether the vfat filesystem is banned from mounting...", "OK")

    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.InsertSection')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.Display')
    @patch('secScanner.enhance.euler.check.C01107_filesystemmod.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_modprobe_ok_but_no_install_rule(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：modprobe 命令成功但输出不含 install /bin/true 时应判定为未禁用"""
        # Mock test setup.
        def side_effect(cmd):
            if cmd.startswith('modprobe'):
                return (0, 'insmod /lib/modules/cramfs.ko')
            return (1, '')

        mock_getstatusoutput.side_effect = side_effect

        # Mock test setup.
        secScanner.enhance.euler.check.C01107_filesystemmod.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01107_filesystemmod()

        # Mock test setup.
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        self.assertEqual(mock_file().write.call_count, 15)
        mock_logger.warning.assert_any_call("WRN_C01107_%02d: %s", 1, WRN_C01107_01)
        mock_Display.assert_any_call("- The squashfs filesystem is not banned from mounting...", "WARNING")

if __name__ == '__main__':
    unittest.main()
