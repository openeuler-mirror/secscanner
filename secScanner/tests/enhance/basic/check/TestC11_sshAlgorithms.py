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
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C11_sshAlgorithms import C11_sshAlgorithms

# 定义测试类
class TestC11_sshAlgorithms(unittest.TestCase):
    def setUp(self):
        # 定义测试时使用的常量和消息
        self.test_data = "/etc/ssh/sshd_config data with SSH algorithms line"

    @patch('secScanner.enhance.basic.check.C11_sshAlgorithms.Display')
    @patch('secScanner.enhance.basic.check.C11_sshAlgorithms.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="KexAlgorithms diffie-hellman-group1-sha1\nCiphers aes128-ctr\nMACs hmac-md5")
    @patch('secScanner.enhance.basic.check.C11_sshAlgorithms.logger')
    def test_algorithms_correctly_set(self, mock_logger, mock_file, mock_insert, mock_display):
        # 运行测试的函数
        C11_sshAlgorithms()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ssh algorithms set, checking ok")

    @patch('secScanner.enhance.basic.check.C11_sshAlgorithms.Display')
    @patch('secScanner.enhance.basic.check.C11_sshAlgorithms.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="#KexAlgorithms diffie-hellman-group1-sha1\n#Ciphers aes128-ctr\n#MACs hmac-md5")
    @patch('secScanner.enhance.basic.check.C11_sshAlgorithms.logger')
    def test_algorithms_not_set(self, mock_logger, mock_file, mock_insert, mock_display):
        # 运行测试的函数
        C11_sshAlgorithms()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C11: %s", WRN_C11)
        mock_logger.warning.assert_any_call("SUG_C11: %s", SUG_C11)


if __name__ == '__main__':
    unittest.main()

