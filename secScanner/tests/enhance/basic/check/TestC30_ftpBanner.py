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
from secScanner.enhance.basic.check.C30_ftpBanner import C30_ftpBanner

class TestC30_ftpBanner(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C30_ftpBanner.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="ftpd_banner=Authorized users only. All activity may be monitored and reported.\n")
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.logger')
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.Display')
    def test_ftp_banner_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C30_ftpBanner()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ftp banner set, checking OK")
        mock_display.assert_called_with("- Check the ftp banner set...", "OK")

    @patch('secScanner.enhance.basic.check.C30_ftpBanner.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="ftpd_banner=Welcome to our server!\n")
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.logger')
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.Display')
    def test_ftp_banner_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C30_ftpBanner()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C30_02: %s", WRN_C30_02)
        mock_logger.warning.assert_any_call("SUG_C30: %s", SUG_C30)
        mock_display.assert_called_with("- Wrong ftp banner config set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C30_ftpBanner.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.logger')
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.Display')
    def test_no_ftp_banner_set(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C30_ftpBanner()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C30_01: %s", WRN_C30_01)
        mock_logger.warning.assert_any_call("SUG_C30: %s", SUG_C30)
        mock_display.assert_called_with("- No ftp banner config set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C30_ftpBanner.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.basic.check.C30_ftpBanner.Display')
    def test_config_file_does_not_exist(self, mock_display, mock_exists, mock_insert):
        # 运行测试的函数
        C30_ftpBanner()

        # 检查是否显示文件不存在的消息
        mock_display.assert_called_with("- Path /etc/vsftpd/vsftpd.conf not exists...", "WARNING")

if __name__ == '__main__':
    unittest.main()

