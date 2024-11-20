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
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C211_rootUIDunique import C211_rootUIDunique

class TestC211_rootUIDunique(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C211_rootUIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, 'root'))
    @patch('secScanner.enhance.level3.check.C211_rootUIDunique.logger')
    @patch('secScanner.enhance.level3.check.C211_rootUIDunique.Display')
    def test_root_uid_unique(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试函数
        C211_rootUIDunique()

        # 验证日志和显示信息
        mock_logger.info.assert_called_with("check root UID unique, checking ok")
        mock_display.assert_called_with("- check root UID unique ...", "OK")

    @patch('secScanner.enhance.level3.check.C211_rootUIDunique.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, 'root admin'))
    @patch('secScanner.enhance.level3.check.C211_rootUIDunique.logger')
    @patch('secScanner.enhance.level3.check.C211_rootUIDunique.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_uid_zero(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试函数
        C211_rootUIDunique()

        # 验证警告信息
        mock_logger.warning.assert_any_call("WRN_C211_01: %s", WRN_C211_01)
        mock_logger.warning.assert_any_call("SUG_C211_01: %s", SUG_C211_01)
        mock_display.assert_called_with("- There are users with UID 0 who are not root ...", "WARNING")

if __name__ == '__main__':
    unittest.main()
