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
from unittest.mock import patch, mock_open, call
import os
import sys
import secScanner
from secScanner.enhance.euler.set.S0364_sysrq import S0364_sysrq

class TestS0364_sysrq(unittest.TestCase):
    # 测试当配置设置为 'yes' 且 /etc/sysctl.conf 文件已经包含正确的 kernel.sysrq=0 设置时的情况
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_set_yes_already_correct(self, mock_file, mock_InsertSection, mock_Display, mock_logger, 
                                           mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]  # /etc/sysctl.conf exists, backup doesn't
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            "some config\n",
            "kernel.sysrq=0\n",
            "other config\n"
        ]

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_copy2.assert_called_once_with('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        mock_add_bak_file.assert_called_once_with('/etc/sysctl.conf_bak')
        mock_Display.assert_called_once_with("- Already right set kernel.sysrq in sysctl config", "FINISHED")
        mock_logger.info.assert_called_once_with("Check set of kernel.sysrq right")

    # 测试当配置设置为 'yes' 且 /etc/sysctl.conf 文件需要更新 kernel.sysrq 设置时的情况
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_set_yes_need_update(self, mock_file, mock_InsertSection, mock_Display, mock_logger, 
                                       mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]  # /etc/sysctl.conf exists, backup doesn't
        mock_file.return_value.__enter__.return_value.readlines.side_effect = [
            ["some config\n", "kernel.sysrq=1\n", "other config\n"],
            ["some config\n", "kernel.sysrq=0\n", "other config\n"]
        ]

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_copy2.assert_called_once_with('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        mock_add_bak_file.assert_called_once_with('/etc/sysctl.conf_bak')
        mock_Display.assert_called_once_with("- Set kernel.sysrq in sysctl config file", "FINISHED")
        mock_logger.info.assert_called_once_with("Set kernel.sysrq finish")

    # 测试当配置设置为 'no' 时的情况,此时应跳过设置
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    def test_sysrq_set_no(self, mock_InsertSection, mock_Display, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'no'

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_Display.assert_called_once_with("Skip set kernel.sysrq due to config file...", "SKIPPING")
        mock_exists.assert_not_called()

    # 测试当 /etc/sysctl.conf 文件不存在时的行为
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    def test_sysrq_set_yes_file_not_exist(self, mock_InsertSection, mock_Display, mock_logger, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False  # /etc/sysctl.conf 不存在

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_Display.assert_called_once_with("- sysctl config file not exist", "FAILED")
        mock_logger.warning.assert_called_once_with("sysctl config file not exist")

    # 测试当需要添加新的 kernel.sysrq=0 设置而不是更新现有设置时的行为
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_set_yes_add_new_setting(self, mock_file, mock_InsertSection, mock_Display, mock_logger, 
                                        mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]  # /etc/sysctl.conf exists, backup doesn't
        
        file_content = ["some config\n", "other config\n"]
        
        def side_effect_read():
            return file_content
        
        def side_effect_write(line):
            file_content.append(line)
        
        mock_file.return_value.__enter__.return_value.readlines.side_effect = side_effect_read
        mock_file.return_value.__enter__.return_value.write.side_effect = side_effect_write

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_copy2.assert_called_once_with('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        mock_add_bak_file.assert_called_once_with('/etc/sysctl.conf_bak')
        
        self.assertTrue(any("kernel.sysrq=0" in line for line in file_content))
        
        mock_Display.assert_called_once_with("- Set kernel.sysrq in sysctl config file", "FINISHED")
        mock_logger.info.assert_called_once_with("Set kernel.sysrq finish")

    # 测试当设置 kernel.sysrq=0 写入失败时的情况
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_set_yes_update_failed(self, mock_file, mock_InsertSection, mock_Display, mock_logger, 
                                        mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]  # /etc/sysctl.conf exists, backup doesn't
        
        file_content = ["some config\n", "kernel.sysrq=1\n", "other config\n"]
        
        mock_file.return_value.__enter__.return_value.readlines.return_value = file_content
        mock_file.return_value.__enter__.return_value.write = lambda x: None  # 模拟写入操作,但不实际修改文件内容

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_copy2.assert_called_once_with('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        mock_add_bak_file.assert_called_once_with('/etc/sysctl.conf_bak')
        
        # 验证 Display 和 logger 调用
        mock_Display.assert_called_once_with("- Set kernel.sysrq in sysctl config", "FAILED")
        mock_logger.warning.assert_called_once_with("Set kernel.sysrq failed")

        # 验证文件内容没有被更改
        mock_file.return_value.__enter__.return_value.readlines.assert_called()
        self.assertEqual(mock_file.return_value.__enter__.return_value.readlines.return_value, file_content)

    # 测试当写入时出现IOError时的情况
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open')
    def test_sysrq_set_yes_setting_failed(self, mock_open, mock_InsertSection, mock_Display, mock_logger, 
                                          mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]  # /etc/sysctl.conf exists, backup doesn't
        
        # 模拟文件读取
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.readlines.return_value = ["some config\n", "kernel.sysrq=1\n", "other config\n"]
        
        # 模拟文件写入失败
        mock_file.write.side_effect = IOError("模拟写入失败")

        S0364_sysrq()

        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_copy2.assert_called_once_with('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        mock_add_bak_file.assert_called_once_with('/etc/sysctl.conf_bak')
        
        # 验证错误处理
        mock_Display.assert_called_once_with("- Set kernel.sysrq in sysctl config", "FAILED")
        mock_logger.warning.assert_called_once_with("Set kernel.sysrq failed")

    # 测试当存在多个 kernel.sysrq 配置时，确保只保留一个正确的配置
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_multiple_configs(self, mock_file, mock_InsertSection, mock_Display, mock_logger,
                                  mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]  # /etc/sysctl.conf exists, backup doesn't

        # 模拟文件中存在多个 kernel.sysrq 配置
        initial_content = [
            "some config\n",
            "kernel.sysrq=1\n",
            "other config\n",
            "kernel.sysrq=0\n",
            "kernel.sysrq=2\n"
        ]
        
        # 期望的最终内容
        expected_content = [
            "some config\n",
            "kernel.sysrq=0\n",
            "other config\n"
        ]

        mock_file_handle = mock_file.return_value.__enter__.return_value
        mock_file_handle.readlines.side_effect = [
            initial_content,  # 第一次读取时返回初始内容
            expected_content  # 第二次读取时返回期望的内容
        ]

        S0364_sysrq()

        # 验证基本调用
        mock_InsertSection.assert_called_once_with("Set config of kernel.sysrq...")
        mock_copy2.assert_called_once_with('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        mock_add_bak_file.assert_called_once_with('/etc/sysctl.conf_bak')

        # 验证写入操作
        write_calls = mock_file_handle.write.call_args_list
        expected_writes = [
            call("some config\n"),
            call("kernel.sysrq=0\n"),
            call("other config\n")
        ]
        self.assertEqual(write_calls, expected_writes)

        # 验证最终状态
        mock_Display.assert_called_once_with("- Set kernel.sysrq in sysctl config file", "FINISHED")
        mock_logger.info.assert_called_once_with("Set kernel.sysrq finish")

    # 测试当存在多个 kernel.sysrq=0 配置时的情况
    @patch('secScanner.enhance.euler.set.S0364_sysrq.seconf.get')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.add_bak_file')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.logger')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.Display')
    @patch('secScanner.enhance.euler.set.S0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_multiple_zero_configs(self, mock_file, mock_InsertSection, mock_Display, mock_logger,
                                       mock_add_bak_file, mock_copy2, mock_exists, mock_seconf_get):
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]

        # 模拟文件中存在多个 kernel.sysrq=0 配置
        initial_content = [
            "some config\n",
            "kernel.sysrq=0\n",
            "other config\n",
            "kernel.sysrq=0\n"
        ]
        
        # 期望的最终内容
        expected_content = [
            "some config\n",
            "kernel.sysrq=0\n",
            "other config\n"
        ]

        mock_file_handle = mock_file.return_value.__enter__.return_value
        mock_file_handle.readlines.side_effect = [
            initial_content,
            expected_content
        ]

        S0364_sysrq()

        # 验证写入操作
        write_calls = mock_file_handle.write.call_args_list
        expected_writes = [
            call("some config\n"),
            call("kernel.sysrq=0\n"),
            call("other config\n")
        ]
        self.assertEqual(write_calls, expected_writes)

        mock_Display.assert_called_once_with("- Set kernel.sysrq in sysctl config file", "FINISHED")
        mock_logger.info.assert_called_once_with("Set kernel.sysrq finish")

if __name__ == '__main__':
    unittest.main()
