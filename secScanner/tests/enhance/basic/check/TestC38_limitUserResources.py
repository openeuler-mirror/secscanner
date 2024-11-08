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
from unittest.mock import patch, MagicMock, mock_open

from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C38_limitUserResources import C38_limitUserResources

class TestC38_limitUserResources(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    def test_all_limits_set_correctly(self):
        # 创建mock_open对象并设置side_effect以根据文件名返回不同内容
        m_open = mock_open()
        limits_conf_data = "* soft stack 10240\n* hard stack 20480\n* hard rss 10000\n* hard nproc 200\n* hard maxlogins 10\n"
        pam_data = "session required /lib/security/pam_limits.so\n"
        file_effects = {'/etc/security/limits.conf': mock_open(read_data=limits_conf_data).return_value,
                        '/etc/pam.d/login': mock_open(read_data=pam_data).return_value}
        
        def side_effect(file_name, *args, **kwargs):
            return file_effects[file_name]
        
        m_open.side_effect = side_effect

        # 使用patch的side_effect功能模拟open
        with patch('builtins.open', m_open), \
             patch('secScanner.enhance.basic.check.C38_limitUserResources.InsertSection') as mock_insert, \
             patch('secScanner.enhance.basic.check.C38_limitUserResources.logger') as mock_logger, \
             patch('secScanner.enhance.basic.check.C38_limitUserResources.Display') as mock_display, \
             patch('os.path.exists', return_value=True):
            C38_limitUserResources()

            mock_logger.info.assert_called_once_with("The system has limit of system resources, checking ok")
            mock_display.assert_called_with("- Check if the limit of system resources is ok...", "OK")

    def test_missing_some_limits(self):
        # 创建mock_open对象并设置side_effect以根据文件名返回不同内容
        m_open = mock_open()
        limits_conf_data = "* soft stack 10240\n* hard nproc 200\n"
        pam_data = "session required /lib/security/pam_limits.so\n"
        file_effects = {'/etc/security/limits.conf': mock_open(read_data=limits_conf_data).return_value,
                        '/etc/pam.d/login': mock_open(read_data=pam_data).return_value,
                        '/var/log/secScanner/check_result.relt': mock_open(read_data="").return_value}
        
        def side_effect(file_name, *args, **kwargs):
            return file_effects[file_name]
        
        m_open.side_effect = side_effect

        # 使用patch的side_effect功能模拟open
        with patch('builtins.open', m_open), \
             patch('secScanner.enhance.basic.check.C38_limitUserResources.InsertSection') as mock_insert, \
             patch('secScanner.enhance.basic.check.C38_limitUserResources.logger') as mock_logger, \
             patch('secScanner.enhance.basic.check.C38_limitUserResources.Display') as mock_display, \
             patch('os.path.exists', return_value=True):
            C38_limitUserResources()

            mock_logger.warning.assert_any_call("WRN_C38: %s", WRN_C38)
            mock_logger.warning.assert_any_call("SUG_C38: %s", SUG_C38)
            mock_display.assert_called_with("- This system has no limit of system resources...", "WARNING")

if __name__ == '__main__':
    unittest.main()

