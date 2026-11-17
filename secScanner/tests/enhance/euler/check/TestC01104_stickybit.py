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
from secScanner.enhance.euler.check.C01104_stickybit import C01104_stickybit  # Mock test setup.

class TestC01104_stickybit(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.Display')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_world_writable_dir_without_sticky_bit(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '/tmp/shared\n/var/tmp/shared')

        # Mock test setup.
        secScanner.enhance.euler.check.C01104_stickybit.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the world writable directories have the sticky bit set")
        mock_getstatusoutput.assert_called_once_with("find / -type d -perm -0002 -a ! -perm -1000 2>/dev/null")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01104\n")
        mock_logger.warning.assert_any_call("WRN_C01104: %s", WRN_C01104)
        mock_logger.warning.assert_any_call("SUG_C01104: %s", SUG_C01104)
        mock_Display.assert_any_call("- Found world writable directories without sticky bit set...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.Display')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_sticky_bit_set(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        C01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the world writable directories have the sticky bit set")
        mock_file.assert_not_called()
        mock_logger.info.assert_any_call("All the world writable directories have the sticky bit set, checking ok")
        mock_Display.assert_any_call("- Check whether the world writable directories have the sticky bit set...", "OK")

    @patch('secScanner.enhance.euler.check.C01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.Display')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_command_failed(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：find 扫描失败（非零退出码）时即使有输出也视为检查通过"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, '/tmp/shared')

        # Mock test setup.
        C01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the world writable directories have the sticky bit set")
        mock_file.assert_not_called()
        mock_Display.assert_any_call("- Check whether the world writable directories have the sticky bit set...", "OK")

    @patch('secScanner.enhance.euler.check.C01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.Display')
    @patch('secScanner.enhance.euler.check.C01104_stickybit.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_whitespace_output_only(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：输出仅含空白字符时应视为无结果"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, ' \n\t ')

        # Mock test setup.
        C01104_stickybit()

        # Mock test setup.
        mock_file.assert_not_called()
        mock_Display.assert_any_call("- Check whether the world writable directories have the sticky bit set...", "OK")

if __name__ == '__main__':
    unittest.main()
