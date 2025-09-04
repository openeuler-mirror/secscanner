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
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C428_ntalkDisabled import C428_ntalkDisabled

class TestC428_ntalkDisabled(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'disabled'))
    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.logger')
    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.Display')
    def test_ntalk_service_disabled(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        C428_ntalkDisabled()
        mock_logger.info.assert_called_with("Has right ntalk service set, checking ok")
        mock_display.assert_called_with("- Has right ntalk service set: disabled...", "OK")

    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'masked'))
    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.logger')
    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.Display')
    def test_ntalk_service_masked(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        C428_ntalkDisabled()
        mock_logger.info.assert_called_with("Has right ntalk service set, checking ok")
        mock_display.assert_called_with("- Has right ntalk service set: masked...", "OK")

    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'Failed to get unit file state'))
    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.logger')
    @patch('secScanner.enhance.level3.check.C428_ntalkDisabled.Display')
    def test_ntalk_service_not_exist(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        C428_ntalkDisabled()
        mock_logger.info.assert_called_with("No ntalk service, checking ok")
        mock_display.assert_called_with("- No ntalk service, checking ok...", "OK")

if __name__ == '__main__':
    unittest.main()
