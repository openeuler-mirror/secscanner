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
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01215_snifftool import C01215_snifftool  # Mock test setup.

class TestC01215_snifftool(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.Display')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_sniff_tools_installed_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'wireshark-3.0.0'), (0, 'netcat-1.0'),
                                            (0, 'tcpdump-4.9.2'), (0, 'nmap-7.70'), (0, 'ethereal-1.0')]

        # Mock test setup.
        secScanner.enhance.euler.check.C01215_snifftool.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01215_snifftool()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the network sniff tools are installed in your Linux System")
        sniffTools = ["wireshark", "netcat", "tcpdump", "nmap", "ethereal"]
        warnMessage = [WRN_C01215_01, WRN_C01215_02, WRN_C01215_03, WRN_C01215_04, WRN_C01215_05]
        sugMessage = [SUG_C01215_01, SUG_C01215_02, SUG_C01215_03, SUG_C01215_04, SUG_C01215_05]
        for i in range(len(sniffTools)):
            tool = sniffTools[i]
            mock_getstatusoutput.assert_any_call('rpm -q %s' % tool)
            mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
            mock_logger.warning.assert_any_call("WRN_C01215_%02d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C01215_%02d: %s", (i + 1), sugMessage[i])
            mock_Display.assert_any_call("- Check the %s software is installed..." % tool, "WARNING")
        mock_file().write.assert_any_call("\nC01215\n")
        self.assertEqual(mock_file().write.call_count, 5)

    @patch('secScanner.enhance.euler.check.C01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.Display')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_sniff_tools_installed_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(1, 'package wireshark is not installed'), (1, 'package netcat is not installed'),
                                            (1, 'package tcpdump is not installed'), (1, 'package nmap is not installed'),
                                            (1, 'package ethereal is not installed')]

        # Mock test setup.
        secScanner.enhance.euler.check.C01215_snifftool.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01215_snifftool()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the network sniff tools are installed in your Linux System")
        mock_file.assert_not_called()
        mock_logger.warning.assert_not_called()
        sniffTools = ["wireshark", "netcat", "tcpdump", "nmap", "ethereal"]
        for tool in sniffTools:
            mock_getstatusoutput.assert_any_call('rpm -q %s' % tool)
            mock_logger.info.assert_any_call("The %s status is: package %s is not installed" % (tool, tool))
            mock_Display.assert_any_call("- Check the %s software is uninstall..." % tool, "OK")
        self.assertEqual(mock_Display.call_count, 5)

    @patch('secScanner.enhance.euler.check.C01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.Display')
    @patch('secScanner.enhance.euler.check.C01215_snifftool.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_partial_sniff_tools_installed(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：仅 tcpdump 安装，其余未安装，只应告警一次且写入一次 RESULT_FILE"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(1, 'package wireshark is not installed'), (1, 'package netcat is not installed'),
                                            (0, 'tcpdump-4.9.2'), (1, 'package nmap is not installed'),
                                            (1, 'package ethereal is not installed')]

        # Mock test setup.
        secScanner.enhance.euler.check.C01215_snifftool.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01215_snifftool()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the network sniff tools are installed in your Linux System")
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01215\n")
        mock_logger.warning.assert_any_call("WRN_C01215_%02d: %s", 3, WRN_C01215_03)
        mock_logger.warning.assert_any_call("SUG_C01215_%02d: %s", 3, SUG_C01215_03)
        self.assertEqual(mock_logger.warning.call_count, 2)
        mock_Display.assert_any_call("- Check the tcpdump software is installed...", "WARNING")
        mock_Display.assert_any_call("- Check the wireshark software is uninstall...", "OK")
        mock_Display.assert_any_call("- Check the nmap software is uninstall...", "OK")

if __name__ == '__main__':
    unittest.main()
