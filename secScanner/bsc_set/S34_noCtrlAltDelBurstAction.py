import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S34_noCtrlAltDelBurstAction():
    set_prohibit_ctrlaltdel = seconf.get('basic', 'set_prohibit_ctrlaltdel')
    InsertSection("Set the system CtrlAltDel Burst Action...")
    if set_prohibit_ctrlaltdel == 'yes':
        if not os.path.exists('/etc/systemd/system/ctrl-alt-del.target_bak') and os.path.exists('/etc/systemd/system/ctrl-alt-del.target'):
            shutil.copy2('/etc/systemd/system/ctrl-alt-del.target', '/etc/systemd/system/ctrl-alt-del.target_bak')
            os.remove('/etc/systemd/system/ctrl-alt-del.target')
        if not os.path.exists('/usr/lib/systemd/system/ctrl-alt-del.target_bak') and os.path.exists('/usr/lib/systemd/system/ctrl-alt-del.target'):
            shutil.copy2('/usr/lib/systemd/system/ctrl-alt-del.target', '/usr/lib/systemd/system/ctrl-alt-del.target_bak')
            os.remove( '/usr/lib/systemd/system/ctrl-alt-del.target')

        if not os.path.exists('/etc/systemd/system.conf_bak') and os.path.exists('/etc/systemd/system.conf'):
            shutil.copy2('/etc/systemd/system.conf', '/etc/systemd/system.conf_bak')
        # -----------------set the CtrlAltDelBurstAction----------------
        with open('/etc/systemd/system.conf', 'r+') as f:
            lines = f.readlines()
            config_exists = False
            for i, line in enumerate(lines):
                if line.strip().startswith("#CtrlAltDelBurstAction"):
                    config_exists = True
                    lines[i] = lines[i].replace("#", "")
                    if not re.search('none', line):
                        lines[i] = "CtrlAltDelBurstAction=none\n"
                    break
                elif line.strip().startswith("CtrlAltDelBurstAction"):
                    config_exists = True
                    if not re.search('none', line):
                        lines[i] = "CtrlAltDelBurstAction=none\n"
                    break
            if not config_exists:
                lines.append("CtrlAltDelBurstAction=none\n")
            f.seek(0)
            f.writelines(lines)
            f.truncate()
        CHECK_EXIST = 0
        with open('/etc/systemd/system.conf', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('CtrlAltDelBurstAction', line):
                    IS_EXIST = 1
                    temp = line.strip('\n').split('=')
                    if temp[0] == 'CtrlAltDelBurstAction' and temp[1] == 'none':
                        CHECK_EXIST = 1
                        ret, result = subprocess.getstatusoutput('systemctl daemon-reexec')
                        if ret != 0:
                            logger.warning('Command execution failed')
                            Display("- Command execution failed...", "FAILED")
                            sys.exit(1)
        if not config_exists:
            logger.info("set the system CtrlAltDel Burst Action failed, no set option")
            Display("- Set the system CtrlAltDel Burst Action...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("set the system CtrlAltDel Burst Action, wrong setting")
            Display("- Set the system CtrlAltDel Burst Action...", "FAILED")
        else:
            logger.info("set the system CtrlAltDel Burst Action successfully")
            Display("- Set the system CtrlAltDel Burst Action...", "FINISHED")
    else:
        Display("- Skip set system CtrlAltDel Burst Action due to config file...", "SKIPPING")

