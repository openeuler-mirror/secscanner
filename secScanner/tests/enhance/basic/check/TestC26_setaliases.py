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
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C26_setaliases import C26_setaliases

class TestC26_setaliases(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C26_setaliases.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="alias ls='ls -al'\nalias rm='rm -i'\n")
    @patch('secScanner.enhance.basic.check.C26_setaliases.logger')
    @patch('secScanner.enhance.basic.check.C26_setaliases.Display')
    def test_aliases_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C26_setaliases()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ls and rm aliases set, checking OK")
        mock_display.assert_called_with("- Check the ls and rm aliases set...", "OK")

    @patch('secScanner.enhance.basic.check.C26_setaliases.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="alias ls='ls -l'\nalias rm='rm -f'\n")
    @patch('secScanner.enhance.basic.check.C26_setaliases.logger')
    @patch('secScanner.enhance.basic.check.C26_setaliases.Display')
    def test_aliases_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C26_setaliases()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C26_02: %s", WRN_C26_02)
        mock_logger.warning.assert_any_call("SUG_C26: %s", SUG_C26)
        mock_display.assert_called_with("- Wrong ls and rm aliases set...", "WARNING")
if __name__ == '__main__':
    unittest.main()