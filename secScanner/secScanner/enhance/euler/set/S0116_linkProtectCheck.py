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


from secScanner.lib import *
from secScanner.gconfig import *
import shutil
import subprocess
import os

logger = logging.getLogger("secscanner")

def S0116_linkProtectCheck():
	'''
	Funtion: Set the protection of symlinks and hardlinks enabled
	'''
	linkTypes = ["symlinks", "hardlinks"]

	set_link_protection = seconf.get('euler', 'set_link_protection')
	InsertSection("Enable Protection of symlinks and hardlinks...")

	if set_link_protection == 'yes':
		for i in range(len(linkTypes)):
			linkType = linkTypes[i]
			protectFlag = "fs.protected_%s" % linkType

			result_symlinks = subprocess.run(['sysctl', protectFlag], capture_output=True)
			resultStr = result_symlinks.stdout.strip().decode("utf-8")
			if resultStr[-1] == '0':
				try:
					enableCmd = "%s=1" % (protectFlag)
					set_result = subprocess.run(["sysctl", "-w", enableCmd], capture_output=True)
				except Exception:
					os.system('sysctl -w fs.protected_symlinks=1')

				if set_result.returncode == 0:
					logger.info("Enable the protection of %s, checking ok" % linkType)
					Display("- Enable the protection of %s..." % linkType, "FINISHED")
				else:
					logger.info("Enable the protection of %s failed" % linkType)
					Display("- Enable the protection of %s..." % linkType, "FAILED")
			else:
				Display("- Protection of %s has already been enabled..." % linkType, "SKIPPING")
	else:
		Display("- Skip enable the protection of symlinks and hardlinks...", "SKIPPING")
