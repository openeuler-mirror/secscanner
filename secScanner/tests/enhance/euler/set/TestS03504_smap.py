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
from unittest.mock import patch, MagicMock
import logging
from secScanner.enhance.euler.set.S03504_smap import S03504_smap

GRUB_FILE = "/boot/efi/EFI/openEuler/grub.cfg"


def _make_open(files, written, opened):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(files.get(path, []))
        else:
            handle.writelines.side_effect = lambda lines: written.extend((path, line) for line in lines)
        return handle
    return _open


def _make_exists(paths):
    return lambda path: path in paths


class TestS03504_smap(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03504_smap.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03504_smap.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03504_smap.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.set.S03504_smap.Display')
    @patch('secScanner.enhance.euler.set.S03504_smap.logger')
    @patch('secScanner.enhance.euler.set.S03504_smap.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open({}, written, opened)):
            S03504_smap()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_smap')
        mock_InsertSection.assert_called_once_with("Set the kernel SMAP enabled...")
        self.assertEqual(opened, [])
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set kernel SMAP due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03504_smap.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03504_smap.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03504_smap.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.set.S03504_smap.Display')
    @patch('secScanner.enhance.euler.set.S03504_smap.logger')
    @patch('secScanner.enhance.euler.set.S03504_smap.seconf.get')
    def test_remove_nosmap_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                    mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists({GRUB_FILE})
        files = {GRUB_FILE: ['linux /vmlinuz nosmap root=/dev/mapper/openeuler-root ro\n', 'chainloader\n']}
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            S03504_smap()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_smap')
        mock_InsertSection.assert_called_once_with("Set the kernel SMAP enabled...")
        self.assertEqual(opened, [(GRUB_FILE, "r", None), (GRUB_FILE, "w", None)])
        mock_copy2.assert_called_once_with(GRUB_FILE, GRUB_FILE + "_bak")
        mock_add_bak_file.assert_called_once_with(GRUB_FILE + "_bak")
        self.assertEqual(written, [
            (GRUB_FILE, 'linux /vmlinuz  root=/dev/mapper/openeuler-root ro\n'),
            (GRUB_FILE, 'chainloader\n'),
        ])
        mock_logger.info.assert_called_once_with("Remove nosmap from grub.cfg finish")
        mock_Display.assert_called_once_with("- Remove nosmap from grub.cfg...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03504_smap.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03504_smap.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03504_smap.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.set.S03504_smap.Display')
    @patch('secScanner.enhance.euler.set.S03504_smap.logger')
    @patch('secScanner.enhance.euler.set.S03504_smap.seconf.get')
    def test_nosmap_not_found_skipping_boundary(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                                mock_add_bak_file, mock_copy2, mock_exists):
        """边界：grub.cfg 存在但不含 nosmap，不修改文件，应视为跳过"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists({GRUB_FILE})
        files = {GRUB_FILE: ['linux /vmlinuz root=/dev/mapper/openeuler-root ro\n']}
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            S03504_smap()

        # Mock test setup.
        self.assertEqual(opened, [(GRUB_FILE, "r", None)])
        self.assertEqual(written, [])
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_logger.info.assert_called_once_with("nosmap not found in grub.cfg")
        mock_Display.assert_called_once_with("- nosmap not found in grub.cfg...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03504_smap.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03504_smap.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03504_smap.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03504_smap.InsertSection')
    @patch('secScanner.enhance.euler.set.S03504_smap.Display')
    @patch('secScanner.enhance.euler.set.S03504_smap.logger')
    @patch('secScanner.enhance.euler.set.S03504_smap.seconf.get')
    def test_grub_file_not_exist_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                        mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open({}, written, opened)):
            S03504_smap()

        # Mock test setup.
        self.assertEqual(opened, [])
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_logger.warning.assert_called_once_with("grub.cfg not exist")
        mock_Display.assert_called_once_with("- grub.cfg not exist...", "FAILED")

if __name__ == '__main__':
    unittest.main()
