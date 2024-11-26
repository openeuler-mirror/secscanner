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
from secScanner.enhance.euler.check.C0243_enANDdePolicy import C0243_enANDdePolicy
import secScanner

class TestC0243_enANDdePolicy(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.InsertSection')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.logger')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_exists(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟文件不存在
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0243_enANDdePolicy.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0243_enANDdePolicy()
        mock_InsertSection.assert_any_call("check global encryption and decryption policies set...")
        mock_logger.warning.assert_any_call("WRN_C0243_02: %s", WRN_C0243_02)
        mock_logger.warning.assert_any_call("SUG_C0243_02: %s", SUG_C0243_02)
        mock_display.assert_any_call("- file /etc/crypto-policies/config does not exist...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.InsertSection')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.logger')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.Display')
    @patch('builtins.open', new_callable=mock_open, read_data="DEFAULT policy set\n")
    def test_policy_set(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟文件存在
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0243_enANDdePolicy.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0243_enANDdePolicy()
        mock_InsertSection.assert_any_call("check global encryption and decryption policies set...")
        mock_logger.info.assert_any_call("Confirm that global encryption and decryption policies have been set")
        mock_display.assert_any_call("- check global encryption and decryption policies set...", "OK")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.InsertSection')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.logger')
    @patch('secScanner.enhance.euler.check.C0243_enANDdePolicy.Display')
    @patch('builtins.open', new_callable=mock_open, read_data="# DEFAULT policy set\n")
    def test_policy_not_set(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟文件存在
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0243_enANDdePolicy.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0243_enANDdePolicy()
        mock_InsertSection.assert_any_call("check global encryption and decryption policies set...")
        mock_logger.warning.assert_any_call("WRN_C0243_01: %s", WRN_C0243_01)
        mock_logger.warning.assert_any_call("SUG_C0243_01: %s", SUG_C0243_01)
        mock_display.assert_any_call("- No global encryption and decryption policy set ...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()