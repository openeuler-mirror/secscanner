import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil


def S26_disableUnUsedaliases():
    SET_DISABLE_UNUSED_ALIASES = seconf.get('advance', 'disable_unused_aliases')
    UNUSED_ALIASES_VALUE = seconf.get('advance', 'unused_aliases_value').split()
    InsertSection("Disable the unused aliases")
    if SET_DISABLE_UNUSED_ALIASES == 'yes':
        if os.path.exists('/etc/aliases'):
            if not os.path.exists('/etc/aliases_bak'):
                shutil.copy2('/etc/aliases', '/etc/aliases_bak')

            with open('/etc/aliases', 'r') as read_file:
                lines = read_file.readlines()
            with open('/etc/aliases', 'w') as write_file:
                for line in lines:
                    temp = line.strip('\n').split(':')
                    if len(temp) == 2 and not '#' in temp[0] and temp[0] in UNUSED_ALIASES_VALUE:
                        print(f"disable alias: {temp[0]}")
                        write_str = '#' + line
                        write_file.write(write_str)
                    else:
                        write_file.write(line)

            subprocess.run(['newaliases'])
            Display(f"- Disable the unused aliases in /etc/aliases...", "FINISHED")
        elif os.path.exists('/etc/mail/aliases'):
            if not os.path.exists('/etc/mail/aliases_bak'):
                shutil.copy2('/etc/mail/aliases', '/etc/mail/aliases_bak')

            with open('/etc/mail/aliases', 'r') as read_file:
                lines = read_file.readlines()
            with open('/etc/mail/aliases', 'w') as write_file:
                for line in lines:
                    temp = line.split(':')
                    if len(temp) == 2 and not '#' in temp[0] and temp[0] in UNUSED_ALIASES_VALUE:
                        print(f"disable alias: {temp[0]}")
                        write_str = '#' + line
                        write_file.write(write_str)
                    else:
                        write_file.write(line)

            subprocess.run(['newaliases'])

            logger.info("disable the unused aliases in /etc/mail/aliases successfully")
            Display(f"- Disable the unused aliases in /etc/mail/aliases...", "FINISHED")
        else:
            Display(f"- Skip disable the unused aliases, due to config file...", "SKIPPING")
    else:
        Display(f"- Skip disable the unused aliases, due to config file...", "SKIPPING")



