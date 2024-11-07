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
from secScanner.enhance.basic.check.C37_Kernelopps import C37_Kernelopps

class TestC37_Kernelopps(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C37_Kernelopps.InsertSection')
    @patch('os.path.exists', side_effect=lambda filepath: filepath in ['/etc/sysctl.conf', '/etc/rc.local'])
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.panic_on_oops=1\n")
    @patch('secScanner.enhance.basic.check.C37_Kernelopps.logger')
    @patch('secScanner.enhance.basic.check.C37_Kernelopps.Display')
    def test_kernel_panic_on_oops_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C37_Kernelopps()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has kernel panic on oops set set, checking OK")
        mock_display.assert_called_with("- Check kernel panic on oops set set...", "OK")

    @patch('secScanner.enhance.basic.check.C37_Kernelopps.InsertSection')
    @patch('os.path.exists', side_effect=lambda filepath: filepath == '/etc/sysctl.conf')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.panic_on_oops=0\n")
    @patch('secScanner.enhance.basic.check.C37_Kernelopps.logger')
    @patch('secScanner.enhance.basic.check.C37_Kernelopps.Display')
    def test_kernel_panic_on_oops_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C37_Kernelopps()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C37_02: %s", WRN_C37_02)
        mock_logger.warning.assert_any_call("SUG_C37: %s", SUG_C37)
        mock_display.assert_called_with("- Wrong kernel panic on oops set set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

