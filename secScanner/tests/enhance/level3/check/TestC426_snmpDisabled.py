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
from secScanner.enhance.level3.check.C426_snmpDisabled import C426_snmpDisabled

class TestC426_snmpDisabled(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C426_snmpDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'disabled'))
    @patch('secScanner.enhance.level3.check.C426_snmpDisabled.logger')
    @patch('secScanner.enhance.level3.check.C426_snmpDisabled.Display')
    def test_snmp_service_disabled(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        C426_snmpDisabled()
        mock_logger.info.assert_called_with("Has right snmpd service set, checking ok")
        mock_display.assert_called_with("- Has right snmpd service set: disabled...", "OK")

    @patch('secScanner.enhance.level3.check.C426_snmpDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'masked'))
    @patch('secScanner.enhance.level3.check.C426_snmpDisabled.logger')
    @patch('secScanner.enhance.level3.check.C426_snmpDisabled.Display')
    def test_snmp_service_masked(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        C426_snmpDisabled()
        mock_logger.info.assert_called_with("Has right snmpd service set, checking ok")
        mock_display.assert_called_with("- Has right snmpd service set: masked...", "OK")

if __name__ == '__main__':
    unittest.main()
