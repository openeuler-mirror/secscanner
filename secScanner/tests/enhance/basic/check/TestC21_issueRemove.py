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
from secScanner.lib.textInfo_basic import *
from secScanner.commands.check_outprint import *
from secScanner.enhance.basic.check.C21_issueRemove import C21_issueRemove

class TestC21_issueRemove(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C21_issueRemove.InsertSection')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.get_value', return_value=0)
    @patch('os.path.exists', side_effect=[True, True])  # Both /etc/issue and /etc/issue.net exist
    @patch('secScanner.enhance.basic.check.C21_issueRemove.logger')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.Display')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.open')
    def test_issue_files_exist_non_vm(self, mock_open, mock_display, mock_logger, mock_exists, mock_get_value, mock_insert):
        # 运行测试的函数
        C21_issueRemove()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C21 :%s", WRN_C21)
        mock_display.assert_called_with("- Check if there is issue file...", "WARNING")

    @patch('secScanner.enhance.basic.check.C21_issueRemove.InsertSection')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.get_value', return_value=0)
    @patch('os.path.exists', side_effect=[False, False])  # Both /etc/issue and /etc/issue.net do not exist
    @patch('secScanner.enhance.basic.check.C21_issueRemove.logger')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.Display')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.open')
    def test_no_issue_files_non_vm(self, mock_open, mock_display, mock_logger, mock_exists, mock_get_value, mock_insert):
        # 运行测试的函数
        C21_issueRemove()

        # 检查预期的OK信息是否已正确记录
        mock_logger.info.assert_called_with("There is no issue file remain, check ok")
        mock_display.assert_called_with("- Check if there is issue file...", "OK")

if __name__ == '__main__':
    unittest.main()
