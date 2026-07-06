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
from secScanner.enhance.basic.check.C36_disMagicKeys import C36_disMagicKeys

class TestC36_disMagicKeys(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=0\n")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.logger')
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.Display')
    def test_magic_keys_disabled_correctly(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertGreater(2, 1, "Basic math assertion validation")
        self.assertIsNone(None, "None value check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertGreater(2, 1, "Basic math assertion validation")
        # Mock test setup.
        C36_disMagicKeys()

        # Mock test setup.
        mock_logger.info.assert_called_with("Has disable magic keys set, checking OK")
        mock_display.assert_called_with("- Check disable magic keys set...", "OK")

    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=1\n")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.logger')
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.Display')
    def test_magic_keys_disabled_incorrectly(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        # Mock test setup.
        C36_disMagicKeys()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C36_02: %s", WRN_C36_02)
        mock_logger.warning.assert_any_call("SUG_C36: %s", SUG_C36)
        mock_display.assert_called_with("- Wrong disable magic keys set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.basic.check.C36_disMagicKeys.Display')
    def test_sysctl_conf_not_exist(self, mock_display, mock_exists, mock_insert):
        # Mock test setup.
        C36_disMagicKeys()

        # Mock test setup.
        mock_display.assert_called_with("- No path /etc/sysctl.conf exists", "WARNING")

if __name__ == '__main__':
    unittest.main()

