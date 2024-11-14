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
from secScanner.enhance.basic.check.C27_syslogProperty import C27_syslogProperty

class TestC27_syslogProperty(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C27_syslogProperty.InsertSection')
    @patch('os.path.exists', side_effect=lambda x: x in ['/etc/rsyslog.conf', '/var/log/messages'])
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw------- 1 root root 123456 Jul 10 10:00 /var/log/messages"))
    @patch('builtins.open', new_callable=mock_open, read_data="*.* /var/log/messages\n")
    @patch('secScanner.enhance.basic.check.C27_syslogProperty.logger')
    @patch('secScanner.enhance.basic.check.C27_syslogProperty.Display')
    def test_logfile_permissions_correct(self, mock_display, mock_logger, mock_file, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C27_syslogProperty()

        # 验证权限正确时的操作
        mock_display.assert_called_with("- check if /var/log/messages property is 600 ...", "OK")

    @patch('secScanner.enhance.basic.check.C27_syslogProperty.InsertSection')
    @patch('os.path.exists', side_effect=lambda x: x in ['/etc/rsyslog.conf', '/var/log/messages'])
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw-r--r-- 1 root root 123456 Jul 10 10:00 /var/log/messages"))
    @patch('builtins.open', new_callable=mock_open, read_data="*.* /var/log/messages\n")
    @patch('secScanner.enhance.basic.check.C27_syslogProperty.logger')
    @patch('secScanner.enhance.basic.check.C27_syslogProperty.Display')
    def test_logfile_permissions_incorrect(self, mock_display, mock_logger, mock_file, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C27_syslogProperty()

        # 验证权限不正确时的操作
        mock_logger.warning.assert_any_call("WRN_C27: %s", WRN_C27)
        mock_logger.warning.assert_any_call("SUG_C27: %s", SUG_C27)
        mock_display.assert_called_with("- Check if /var/log/messages property is not 600...", "WARNING")
    
    @patch('secScanner.enhance.basic.check.C27_syslogProperty.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.basic.check.C27_syslogProperty.Display')
    def test_rsyslog_conf_not_exist(self, mock_display, mock_exists, mock_insert):
        # 运行测试的函数
        C27_syslogProperty()

        # 验证配置文件不存在时的操作
        mock_display.assert_called_with("- file '/etc/rsyslog.conf' does not exist...", "SKIPPED")


if __name__ == '__main__':
    unittest.main()
