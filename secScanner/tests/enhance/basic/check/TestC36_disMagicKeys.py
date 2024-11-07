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
from secScanner.enhance.basic.check.C36_disMagicKeys import C36_disMagicKeys

class TestC36_disMagicKeys(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=0\n")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.logger')
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.Display')
    def test_magic_keys_disabled_correctly(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        # 运行测试的函数
        C36_disMagicKeys()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has disable magic keys set, checking OK")
        mock_display.assert_called_with("- Check disable magic keys set...", "OK")

    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=1\n")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.logger')
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.Display')
    def test_magic_keys_disabled_incorrectly(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        # 运行测试的函数
        C36_disMagicKeys()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C36_02: %s", WRN_C36_02)
        mock_logger.warning.assert_any_call("SUG_C36: %s", SUG_C36)
        mock_display.assert_called_with("- Wrong disable magic keys set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

