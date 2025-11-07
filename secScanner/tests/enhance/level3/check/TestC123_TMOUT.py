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
from secScanner.lib.textInfo_level3 import *

class TestC123_TMOUT(unittest.TestCase):

    @patch("secScanner.enhance.level3.check.C123_TMOUT.InsertSection")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.open", new_callable=mock_open, read_data="TMOUT=300\n")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.logger")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.Display")
    def test_tmout_correct_setting(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.level3.check.C123_TMOUT.C123_TMOUT()
        mock_logger.info.assert_any_call("Has right TMOUT set, checking ok")
        mock_display.assert_any_call("- Has right TMOUT set ...", "OK")

    @patch("secScanner.enhance.level3.check.C123_TMOUT.InsertSection")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.open", new_callable=mock_open, read_data="TMOUT=600\n")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.logger")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.Display")
    def test_tmout_incorrect_setting(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.level3.check.C123_TMOUT.C123_TMOUT()
        mock_logger.warning.assert_any_call("WRN_C123_02: %s", WRN_C123_02)
        mock_logger.warning.assert_any_call("SUG_C123: %s", SUG_C123)
        mock_display.assert_any_call("- Wrong TMOUT set, must less than 300...", "WARNING")

    @patch("secScanner.enhance.level3.check.C123_TMOUT.InsertSection")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.open", new_callable=mock_open, read_data="# TMOUT setting is commented out")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.logger")
    @patch("secScanner.enhance.level3.check.C123_TMOUT.Display")
    def test_tmout_not_set(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.level3.check.C123_TMOUT.C123_TMOUT()
        mock_logger.warning.assert_any_call("WRN_C123_01: %s", WRN_C123_01)
        mock_logger.warning.assert_any_call("SUG_C123: %s", SUG_C123)
        mock_display.assert_any_call("- No TMOUT set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

