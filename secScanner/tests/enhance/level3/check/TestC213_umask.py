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

class TestC213_umask(unittest.TestCase):

    @patch("secScanner.enhance.level3.check.C213_umask.InsertSection")
    @patch("secScanner.enhance.level3.check.C213_umask.open", new_callable=mock_open, read_data="umask 027\n")
    @patch("secScanner.enhance.level3.check.C213_umask.logger")
    @patch("secScanner.enhance.level3.check.C213_umask.Display")
    def test_umask_correct_setting(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.level3.check.C213_umask.C213_umask()
        mock_logger.info.assert_any_call("Has right umask set, checking ok")
        mock_display.assert_any_call("- Has right umask set...", "OK")
    
    @patch("secScanner.enhance.level3.check.C213_umask.InsertSection")
    @patch("secScanner.enhance.level3.check.C213_umask.open", new_callable=mock_open, read_data="umask 022\n")
    @patch("secScanner.enhance.level3.check.C213_umask.logger")
    @patch("secScanner.enhance.level3.check.C213_umask.Display")
    def test_umask_incorrect_setting(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.level3.check.C213_umask.C213_umask()
        mock_logger.warning.assert_any_call("WRN_C213: %s", WRN_C213)
        mock_logger.warning.assert_any_call("SUG_C213: %s", SUG_C213)
        mock_display.assert_called_with("- Wrong umask set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

