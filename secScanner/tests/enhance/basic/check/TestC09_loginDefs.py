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
from secScanner.lib.textInfo_basic import *

class TestC09_loginDefs(unittest.TestCase):
    @patch('secScanner.enhance.basic.check.C09_loginDefs.InsertSection')
    @patch('secScanner.enhance.basic.check.C09_loginDefs.open', new_callable=mock_open, read_data="PASS_MAX_DAYS 90\nPASS_MIN_DAYS 5\nPASS_MIN_LEN 8\nPASS_WARN_AGE 30\n")
    @patch('secScanner.enhance.basic.check.C09_loginDefs.logger')
    @patch('secScanner.enhance.basic.check.C09_loginDefs.Display')
    #@patch('secScanner.enhance.basic.check.C09_loginDefs.InsertSection')
    def test_values_meet_requirements(self, mock_display, mock_logger, mock_file, mock_insert):
        """所有配置值都符合要求的情况"""
        secScanner.enhance.basic.check.C09_loginDefs.C09_loginDefs()
        mock_logger.info.assert_called_with("PASS_WARN_AGE value is safe, checking OK")
        mock_display.assert_called_with("- Check the PASS_WARN_AGE value...", "OK")

    @patch('secScanner.enhance.basic.check.C09_loginDefs.InsertSection')
    @patch('secScanner.enhance.basic.check.C09_loginDefs.open', new_callable=mock_open, read_data="PASS_MAX_DAYS 98\nPASS_MIN_DAYS 3\nPASS_MIN_LEN 6\nPASS_WARN_AGE 20\n")
    @patch('secScanner.enhance.basic.check.C09_loginDefs.logger')
    @patch('secScanner.enhance.basic.check.C09_loginDefs.Display')
    #@patch('secScanner.enhance.basic.check.C09_loginDefs.InsertSection')
    def test_values_do_not_meet_requirements(self, mock_display, mock_logger, mock_file, mock_insert):
        """配置值不符合要求的情况"""
        secScanner.enhance.basic.check.C09_loginDefs.C09_loginDefs()
        mock_logger.warning.assert_any_call("WRN_C09_01: %s", WRN_C09_01)
        mock_display.assert_any_call("- PASS_MAX_DAYS value is not safe...", "WARNING")


# 如果是作为脚本运行，自动执行测试
if __name__ == '__main__':
    unittest.main()

