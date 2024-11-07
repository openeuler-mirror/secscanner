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
from secScanner.enhance.basic.check.C13_restrictFTPdir import C13_restrictFTPdir

# 定义测试类
class TestC13_restrictFTPdir(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C13_restrictFTPdir.Display')
    @patch('secScanner.enhance.basic.check.C13_restrictFTPdir.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="chroot_local_user=YES\nchroot_list_enable=YES\nchroot_list_file=/etc/vsftpd/chroot_list\n")
    @patch('secScanner.enhance.basic.check.C13_restrictFTPdir.logger')
    def test_all_settings_correct(self, mock_logger, mock_file, mock_exists, mock_insert, mock_display):
        # 运行测试的函数
        C13_restrictFTPdir()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ftp restrict directories set, checking OK")

    @patch('secScanner.enhance.basic.check.C13_restrictFTPdir.Display')
    @patch('secScanner.enhance.basic.check.C13_restrictFTPdir.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="chroot_local_user=NO\nchroot_list_enable=NO\nchroot_list_file=wrong_path\n")
    @patch('secScanner.enhance.basic.check.C13_restrictFTPdir.logger')
    def test_settings_incorrect(self, mock_logger, mock_file, mock_exists, mock_insert, mock_display):
        # 运行测试的函数
        C13_restrictFTPdir()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C13_02: %s", WRN_C13_02)
        mock_logger.warning.assert_any_call("SUG_C13: %s", SUG_C13)


if __name__ == '__main__':
    unittest.main()

