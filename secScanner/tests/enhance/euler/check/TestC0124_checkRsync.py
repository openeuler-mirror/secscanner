import unittest
from unittest.mock import patch, MagicMock, mock_open
from secScanner.enhance.euler.check.C0124_checkRsync import C0124_checkRsync, logger, Display, RESULT_FILE, WRN_C0124, SUG_C0124

class TestC0124_checkRsync(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0124_checkRsync.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0124_checkRsync.logger')
    @patch('secScanner.enhance.euler.check.C0124_checkRsync.Display')
    def test_rsync_not_installed(self, mock_Display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟rsync未安装
        mock_getstatusoutput.return_value = (1, 'package rsync is not installed')
        # 调用测试函数
        C0124_checkRsync()
        mock_InsertSection.assert_called_once_with("Check the rsyncd server's status in your Linux System ")
        mock_logger.info.assert_called_with('The status of Rsync is :package rsync is not installed')
        mock_Display.assert_called_with('-The Status is package rsync is not installed of Rsync...', 'OK')

    @patch('secScanner.enhance.euler.check.C0124_checkRsync.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0124_checkRsync.logger')
    @patch('secScanner.enhance.euler.check.C0124_checkRsync.Display')
    def test_rsync_installed_disabled(self, mock_Display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟rsync已安装，服务未启用
        mock_getstatusoutput.side_effect = [
            (0, 'rsync-3.1.2-1.el7.x86_64'),
            (3, 'disabled')
        ]
        # 调用测试函数
        C0124_checkRsync()
        mock_InsertSection.assert_called_once_with("Check the rsyncd server's status in your Linux System ")
        mock_logger.info.assert_any_call('The status of Rsync is :rsync-3.1.2-1.el7.x86_64')
        mock_logger.info.assert_any_call('The status of rsyncd is disabled')
        mock_Display.assert_called_with("- Check the status of rsyncd is disabled...","OK")

if __name__ == '__main__':
    unittest.main()