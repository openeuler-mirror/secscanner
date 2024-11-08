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
from secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction import C34_noCtrlAltDelBurstAction

class TestC34_noCtrlAltDelBurstAction(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.InsertSection')
    @patch('os.path.exists', side_effect=lambda x: x not in ["/etc/systemd/system/ctrl-alt-del.target_bak", "/usr/lib/systemd/system/ctrl-alt-del.target"])
    @patch('builtins.open', new_callable=mock_open, read_data="CtrlAltDelBurstAction=none\n")
    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.logger')
    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.Display')
    def test_ctrlaltdel_burst_action_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C34_noCtrlAltDelBurstAction()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has system CtrlAltDel burst action set, checking OK")
        mock_display.assert_called_with("- Check the system CtrlAltDel burst action...", "OK")

    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.InsertSection')
    @patch('os.path.exists', side_effect=lambda x: x not in ["/etc/systemd/system/ctrl-alt-del.target_bak", "/usr/lib/systemd/system/ctrl-alt-del.target"])
    @patch('builtins.open', new_callable=mock_open, read_data="CtrlAltDelBurstAction=reboot\n")
    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.logger')
    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.Display')
    def test_ctrlaltdel_burst_action_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C34_noCtrlAltDelBurstAction()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C34_02: %s", WRN_C34_02)
        mock_logger.warning.assert_any_call("SUG_C34: %s", SUG_C34)
        mock_display.assert_called_with("- Wrong system CtrlAltDel burst action config set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.InsertSection')
    @patch('os.path.exists', side_effect=lambda x: x not in ["/etc/systemd/system/ctrl-alt-del.target_bak", "/usr/lib/systemd/system/ctrl-alt-del.target"])
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.logger')
    @patch('secScanner.enhance.basic.check.C34_noCtrlAltDelBurstAction.Display')
    def test_no_ctrlaltdel_burst_action_set(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C34_noCtrlAltDelBurstAction()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C34_01: %s", WRN_C34_01)
        mock_logger.warning.assert_any_call("SUG_C34: %s", SUG_C34)
        mock_display.assert_called_with("- No system CtrlAltDel burst action config set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

