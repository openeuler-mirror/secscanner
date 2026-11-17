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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01101_nouserfiles import C01101_nouserfiles  # Mock test setup.

class TestC01101_nouserfiles(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_nouser_and_nogroup_found(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, '/tmp/orphan_file'), (0, '/tmp/orphan_dir')]

        # Mock test setup.
        secScanner.enhance.euler.check.C01101_nouserfiles.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files or directories without owner or group")
        findTypes = ["nouser", "nogroup"]
        warnMessage = [WRN_C01101_01, WRN_C01101_02]
        sugMessage = [SUG_C01101_01, SUG_C01101_02]
        for i in range(len(findTypes)):
            findType = findTypes[i]
            mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
            mock_logger.warning.assert_any_call("WRN_C01101_%02d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C01101_%02d: %s", (i + 1), sugMessage[i])
            mock_Display.assert_any_call("- Found files or directories without %s..." % findType, "WARNING")

    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.logger')
    def test_no_nouser_nogroup_found(self, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, ''), (0, '')]

        # Mock test setup.
        C01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files or directories without owner or group")
        findTypes = ["nouser", "nogroup"]
        for findType in findTypes:
            mock_logger.info.assert_any_call("No file or directory without %s found, checking ok", findType)
            mock_Display.assert_any_call("- Check whether files or directories without %s exist..." % findType, "OK")

    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.logger')
    def test_find_command_failed(self, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(1, ''), (1, '')]

        # Mock test setup.
        C01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files or directories without owner or group")
        findTypes = ["nouser", "nogroup"]
        for findType in findTypes:
            mock_Display.assert_any_call("- Check whether files or directories without %s exist..." % findType, "OK")

    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.check.C01101_nouserfiles.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_nouser_found_nogroup_whitespace_only(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：nouser 有结果，nogroup 输出仅空白字符应视为无结果"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, '/tmp/orphan_file'), (0, ' \n\t')]

        # Mock test setup.
        secScanner.enhance.euler.check.C01101_nouserfiles.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files or directories without owner or group")
        mock_file().write.assert_called_once_with("\nC01101\n")
        mock_Display.assert_any_call("- Found files or directories without nouser...", "WARNING")
        mock_Display.assert_any_call("- Check whether files or directories without nogroup exist...", "OK")

if __name__ == '__main__':
    unittest.main()
