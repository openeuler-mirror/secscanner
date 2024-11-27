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
from secScanner.enhance.euler.check.C0322_pubkeyTypes import C0322_pubkeyTypes
import secScanner


class TestC0322_pubkeyTypes(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0322_pubkeyTypes.InsertSection')
    @patch('secScanner.enhance.euler.check.C0322_pubkeyTypes.logger')
    @patch('secScanner.enhance.euler.check.C0322_pubkeyTypes.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_file_not_exists(self, mock_exists, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_exists.return_value = False
        config_file = "/etc/ssh/sshd_config"
        secScanner.enhance.euler.check.C0322_pubkeyTypes.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        C0322_pubkeyTypes()
        mock_InsertSection.assert_any_call("Check set of PubkeyAcceptedKeyTypes")
        mock_logger.warning.assert_any_call(f"WRN_C0322: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0322: {config_file} {SUG_no_file}")
        mock_display.assert_any_call(f"- Config file: {config_file} not found...", "SKIPPING")
        mock_open.assert_called_with("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()