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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0213_removeForward import C0213_removeForward
import secScanner

class TestC0213_removeForward(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0213_removeForward.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0213_removeForward.logger')
    @patch('secScanner.enhance.euler.check.C0213_removeForward.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_with_forward_file(self, mock_walk, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟存在.forward文件
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], [".forward"]), ("/home/user2", [], [])]
        secScanner.enhance.euler.check.C0213_removeForward.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0213_removeForward()
        mock_InsertSection.assert_any_call("Confirm the existence of the .forward file in the Home directory")
        mock_logger.warning.assert_any_call("WRN_C0213_01: %s", WRN_C0213_01)
        mock_logger.warning.assert_any_call("SUG_C0213_01: %s", SUG_C0213_01)
        mock_display.assert_called_once_with("- At least one .forward file in the Home directory ...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0213_removeForward.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0213_removeForward.logger')
    @patch('secScanner.enhance.euler.check.C0213_removeForward.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_without_forward_file(self, mock_walk, mock_isdir, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟不存在.forward文件
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, "user1:x:1000:1000::/home/user1:/bin/bash\nuser2:x:1001:1001::/home/user2:/bin/bash")
        mock_isdir.return_value = True
        mock_walk.return_value = [("/home/user1", [], []), ("/home/user2", [], [])]
        # 调用测试函数
        C0213_removeForward()
        mock_InsertSection.assert_any_call("Confirm the existence of the .forward file in the Home directory")
        mock_logger.info.assert_any_call("Confirm the existence of the .forward file in the Home directory, checking ok")
        mock_display.assert_called_once_with("- check if the .forward file in the Home directory...", "OK")

if __name__ == '__main__':
    unittest.main()