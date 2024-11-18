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
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C113_GIDunique import C113_GIDunique

class TestC113_GIDunique(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C113_GIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, ''))
    @patch('secScanner.enhance.level3.check.C113_GIDunique.logger')
    @patch('secScanner.enhance.level3.check.C113_GIDunique.Display')
    def test_gid_unique(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C113_GIDunique()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Confirm GID uniqueness, checking OK")
        mock_display.assert_called_with("- Confirm GID uniqueness...", "OK")

    @patch('secScanner.enhance.level3.check.C113_GIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, '1000\n2000'))
    @patch('secScanner.enhance.level3.check.C113_GIDunique.logger')
    @patch('secScanner.enhance.level3.check.C113_GIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_gids(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C113_GIDunique()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C113_01: %s", WRN_C113_01)
        mock_logger.warning.assert_any_call("SUG_C113_01: %s", SUG_C113_01)

if __name__ == '__main__':
    unittest.main()
