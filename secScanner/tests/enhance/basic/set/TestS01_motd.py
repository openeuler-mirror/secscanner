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
import shutil
import os
import pathlib
import secScanner
from secScanner.enhance.basic.set.S01_motd import S01_motd

class TestS01_motd(unittest.TestCase):

    @patch('secScanner.enhance.basic.set.S01_motd.seconf.get')
    @patch('secScanner.enhance.basic.set.S01_motd.os.path.exists')
    @patch('secScanner.enhance.basic.set.S01_motd.os.path.getsize')
    @patch('secScanner.enhance.basic.set.S01_motd.shutil.copy2')
    @patch('secScanner.enhance.basic.set.S01_motd.open', new_callable=mock_open)
    @patch('secScanner.enhance.basic.set.S01_motd.pathlib.Path.touch')
    @patch('secScanner.enhance.basic.set.S01_motd.os.chmod')
    @patch('secScanner.enhance.basic.set.S01_motd.logger')
    @patch('secScanner.enhance.basic.set.S01_motd.Display')
    @patch('secScanner.enhance.basic.set.S01_motd.InsertSection')
    @patch('secScanner.enhance.basic.set.S01_motd.add_bak_file')
    def test_set_motd(self, mock_add_bak_file, mock_InsertSection, mock_Display, mock_logger, mock_chmod, mock_touch, mock_open, mock_copy2, mock_getsize, mock_exists, mock_get):
        # 设置模拟返回值
        mock_get.side_effect = lambda section, option: 'yes' if option == 'set_motd' else 'Authorized users only. All activity may be monitored and reported'
        # 让 /etc/motd 存在，而 /etc/motd_bak 不存在
        mock_exists.side_effect = lambda path: path == '/etc/motd'

        # 初始化全局变量
        global bak_files_list
        bak_files_list = []

        # 调用测试函数
        S01_motd()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("set /etc/motd banner")
        mock_copy2.assert_called_once_with('/etc/motd', '/etc/motd_bak')
        mock_add_bak_file.assert_called_once_with('/etc/motd_bak')
        mock_touch.assert_not_called()  # 因为 /etc/motd 已存在
        mock_chmod.assert_not_called()  # 因为 /etc/motd 已存在
        mock_open.assert_called_once_with('/etc/motd', "w")
        mock_open().write.assert_called_once_with('Authorized users only. All activity may be monitored and reported')
        mock_Display.assert_called_once_with("- Set motd banner finished...", "FINISHED")
        mock_logger.info.assert_called_once_with("set the motd banner successfully")

    @patch('secScanner.enhance.basic.set.S01_motd.seconf.get')
    @patch('secScanner.enhance.basic.set.S01_motd.os.path.exists')
    @patch('secScanner.enhance.basic.set.S01_motd.logger')
    @patch('secScanner.enhance.basic.set.S01_motd.Display')
    @patch('secScanner.enhance.basic.set.S01_motd.InsertSection')
    def test_skip_set_motd(self, mock_InsertSection, mock_Display, mock_logger, mock_exists, mock_get):
        # 设置模拟返回值
        mock_get.side_effect = lambda section, option: 'no' if option == 'set_motd' else 'Authorized users only. All activity may be monitored and reported'
        mock_exists.return_value = False

        # 调用测试函数
        S01_motd()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("set /etc/motd banner")
        mock_Display.assert_called_once_with("- Skip set motd banner due to config file...", "SKIPPING")
        mock_logger.info.assert_not_called()

if __name__ == '__main__':
    unittest.main()
