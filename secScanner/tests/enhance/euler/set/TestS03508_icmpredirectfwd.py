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
import logging
from secScanner.enhance.euler.set.S03508_icmpredirectfwd import S03508_icmpredirectfwd  # Mock test setup.

redirectParams = ["net.ipv4.conf.all.send_redirects",
                  "net.ipv4.conf.default.send_redirects"]


def _fake_run(value, failed_param=None):
    def fake_run(cmd, **kwargs):
        result = MagicMock()
        result.stdout = b""
        result.returncode = 0
        if len(cmd) == 2:
            result.stdout = ("%s = %s\n" % (cmd[1], value)).encode("utf-8")
        elif failed_param is not None and cmd[2] == "%s=0" % failed_param:
            result.returncode = 1
        return result
    return fake_run


class TestS03508_icmpredirectfwd(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.logger')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03508_icmpredirectfwd()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_icmpredirectfwd')
        mock_InsertSection.assert_called_once_with("Set the system not to send ICMP redirect packets...")
        mock_Display.assert_called_once_with("- Skip set ICMP redirect send parameters due to config file...", "SKIPPING")
        mock_run.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.os.makedirs')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.logger')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_success_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                  mock_InsertSection, mock_run, mock_exists, mock_makedirs):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = _fake_run(1)
        mock_exists.return_value = False

        # Mock test setup.
        S03508_icmpredirectfwd()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_icmpredirectfwd')
        mock_InsertSection.assert_called_once_with("Set the system not to send ICMP redirect packets...")
        self.assertEqual(mock_run.call_count, 5)
        for param in redirectParams:
            mock_run.assert_any_call(['sysctl', param], capture_output=True)
            mock_run.assert_any_call(["sysctl", "-w", "%s=0" % param], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.route.flush=1"], capture_output=True)
        mock_makedirs.assert_called_once_with("/etc/sysctl.d", exist_ok=True)
        mock_file.assert_called_with("/etc/sysctl.d/secscanner.conf", "a")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_logger.info.assert_called_with("Set ICMP redirect send parameters finish")
        mock_Display.assert_called_once_with("- Set ICMP redirect send parameters to 0...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.os.makedirs')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.logger')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                        mock_InsertSection, mock_run, mock_exists, mock_makedirs):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = _fake_run(1, failed_param="net.ipv4.conf.default.send_redirects")
        mock_exists.return_value = False

        # Mock test setup.
        S03508_icmpredirectfwd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the system not to send ICMP redirect packets...")
        self.assertEqual(mock_run.call_count, 5)
        mock_logger.warning.assert_called_once_with("Set ICMP redirect send parameters failed")
        mock_Display.assert_called_once_with("- Set ICMP redirect send parameters to 0...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.logger')
    @patch('secScanner.enhance.euler.set.S03508_icmpredirectfwd.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_already_set_to_0_skipping(self, mock_file, mock_seconf_get, mock_logger,
                                       mock_Display, mock_InsertSection, mock_run):
        """边界：所有参数已为 0，不应执行 sysctl -w，也不应写持久化配置"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = _fake_run(0)

        # Mock test setup.
        S03508_icmpredirectfwd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the system not to send ICMP redirect packets...")
        self.assertEqual(mock_run.call_count, 2)
        for param in redirectParams:
            mock_run.assert_any_call(['sysctl', param], capture_output=True)
        mock_file.assert_not_called()
        mock_logger.info.assert_called_with("ICMP redirect send parameters already set to 0")
        mock_Display.assert_called_once_with("- ICMP redirect send parameters have already been set to 0...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
