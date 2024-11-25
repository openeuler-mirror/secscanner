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
from secScanner.enhance.level3.check.C254_gshadowProperty import C254_gshadowProperty

class TestC254_gshadowProperty(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C254_gshadowProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, "---------- 1 root root 123456 Jul 10 10:00 /etc/gshadow"))
    @patch('secScanner.enhance.level3.check.C254_gshadowProperty.logger')
    @patch('secScanner.enhance.level3.check.C254_gshadowProperty.Display')
    def test_gshadow_permissions_correct(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C254_gshadowProperty()

        # 验证权限正确时的操作
        mock_display.assert_called_with("- check if /etc/gshadow property is 0 ...", "OK")

    @patch('secScanner.enhance.level3.check.C254_gshadowProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw-r--r-- 1 root root 123456 Jul 10 10:00 /etc/gshadow"))
    @patch('secScanner.enhance.level3.check.C254_gshadowProperty.logger')
    @patch('secScanner.enhance.level3.check.C254_gshadowProperty.Display')
    def test_gshadow_permissions_incorrect(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C254_gshadowProperty()

        # 验证权限不正确时的操作
        mock_logger.warning.assert_any_call("WRN_C254: %s", WRN_C254)
        mock_logger.warning.assert_any_call("SUG_C254: %s", SUG_C254)
        mock_display.assert_called_with("- Check if /etc/gshadow property is not 0...", "WARNING")

if __name__ == '__main__':
    unittest.main()
