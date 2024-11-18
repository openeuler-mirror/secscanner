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
import subprocess
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0204_rootUIDunique import C0204_rootUIDunique  # 替换为实际的模块路径

class TestC0204_rootUIDunique(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.Display')
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.InsertSection')
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.os.path.exists')
    @patch('subprocess.getstatusoutput', return_value = (0, "root"))
    def test_uid_is_root(self, mock_subprocess, mock_exists, mock_InsertSection, mock_Display, mock_file):
        # 模拟 /etc/passwd 存在
        mock_exists.return_value = True
        
        # 调用被测试函数
        C0204_rootUIDunique()
        
        # 验证函数行为
        mock_InsertSection.assert_called_with("Check if root UID is unique")
        mock_Display.assert_called_with("- check root UID unique ...", "OK")
    
   
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.logger')
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.Display')
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.InsertSection')
    @patch('secScanner.enhance.euler.check.C0204_rootUIDunique.os.path.exists')
    @patch('subprocess.getstatusoutput', return_value = (0, "user1")) 
    def test_uid_is_not_root(self, mock_subprocess, mock_exists, mock_InsertSection, mock_Display, mock_logger, mock_file):
        # 模拟 /etc/passwd 存在
        mock_exists.return_value = True
        
        # 调用被测试函数
        C0204_rootUIDunique()
        
        # 验证函数行为
        mock_InsertSection.assert_called_with("Check if root UID is unique")
        mock_logger.warning.assert_any_call("WRN_C0204_01: %s", WRN_C0204_01)
        mock_logger.warning.assert_any_call("SUG_C0204_01: %s", SUG_C0204_01)
        mock_Display.assert_called_with("- There are users with UID 0 who are not root ...", "WARNING")

if __name__ == "__main__":
    unittest.main()