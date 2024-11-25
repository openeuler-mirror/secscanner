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
from secScanner.enhance.euler.check.C0301_uncommonNetwork import C0301_uncommonNetwork
import secScanner

class TestC0301_uncommonNetwork(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0301_uncommonNetwork.InsertSection')
    @patch('secScanner.enhance.euler.check.C0301_uncommonNetwork.logger')
    @patch('secScanner.enhance.euler.check.C0301_uncommonNetwork.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_sctp_and_tipc_disabled(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟 sctp 和 tipc 都被禁用的情况
        mock_getstatusoutput.side_effect = [
            (0, "install /bin/true"),  # sctp
            (0, "install /bin/true")   # tipc
        ]
        C0301_uncommonNetwork()
        mock_InsertSection.assert_any_call("Check avoid using uncommon network service")
        mock_display.assert_any_call("- Avoid using uncommon network service...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0301_uncommonNetwork.InsertSection')
    @patch('secScanner.enhance.euler.check.C0301_uncommonNetwork.logger')
    @patch('secScanner.enhance.euler.check.C0301_uncommonNetwork.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_sctp_enabled_and_tipc_disabled(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟 sctp 被启用而 tipc 被禁用的情况
        mock_getstatusoutput.side_effect = [
            (0, "insmod /lib/modules/"),  # sctp
            (0, "install /bin/true")     # tipc
        ]
        C0301_uncommonNetwork()
        secScanner.enhance.euler.check.C0301_uncommonNetwork.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        mock_InsertSection.assert_any_call("Check avoid using uncommon network service")
        mock_logger.warning.assert_any_call("WRN_C0301_03: %s", WRN_C0301_03)
        mock_logger.warning.assert_any_call("SUG_C0301_03: %s", SUG_C0301_03)
        mock_display.assert_any_call("- Check sctp should be avoided...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()