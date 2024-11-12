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
import os
import logging
from secScanner.enhance.euler.check.C0205_fileProperty import C0205_fileProperty  # 确保正确导入 C0205_fileProperty 函数
from secScanner.lib.textInfo_euler import *

class TestC0205_fileProperty(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0205_fileProperty.Display')
    @patch('secScanner.enhance.euler.check.C0205_fileProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('os.stat', side_effect=lambda x: MagicMock(st_mode=(0o100644 if x.endswith('644') else 0o100000)))
    @patch('secScanner.enhance.euler.check.C0205_fileProperty.logger', autospec=True)  # 确保使用正确的 logger 路径
    @patch('builtins.open', new_callable=mock_open)  # Mock the built-in open function
    def test_file_permissions(self, mock_open, mock_logger, mock_stat, mock_exists, mock_insert, mock_display):
        # Assume configuration returns files to check
        with patch('secScanner.enhance.euler.check.C0205_fileProperty.seconf.get', return_value='file644.txt file000.txt'):
            with patch('secScanner.enhance.euler.check.C0205_fileProperty.seconf.options', return_value={'chmod_644_file': True, 'chmod_000_file': True}):
                C0205_fileProperty()
        
        # Verify logs for correct and incorrect permissions
        mock_logger.info.assert_any_call('file644.txt is safe, checking ok')
        mock_logger.warning.assert_any_call('WRN_C0205_1: %s', WRN_C0205_1)
        mock_logger.warning.assert_any_call('SUG_C0205_1: %s', SUG_C0205_1)

if __name__ == '__main__':
    unittest.main()

