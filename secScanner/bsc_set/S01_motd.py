import shutil
from secScanner.lib import *
from secScanner.gconfig import *


def S01_motd():
    InsertSection("set /etc/motd banner")

    set_motd = seconf.get('basic', 'set_motd')
    motd = seconf.get('basic', 'motd')
    if set_motd == 'yes':
        if os.path.exists('/etc/motd') and not os.path.exists('/etc/motd_bak'):
            shutil.copy2('/etc/motd', '/etc/motd_bak')
        elif os.path.exists('/etc/motd'):
            with open('/etc/motd', "w") as write_file: #overwrite ;if /etc/motd not exsit, this line will build a new motd
                write_file.write(motd)
            if os.path.getsize('/etc/motd'):
                Display("- Set motd banner finished...", "FINISHED")
            else:
                Display("- Set motd banner failed...", "FAILED")
        else:
            Display("- filepath /etc/motd not exist...", "SKIPPING")
    else:
        Display("- Skip set motd banner due to config file...", "SKIPPING")



