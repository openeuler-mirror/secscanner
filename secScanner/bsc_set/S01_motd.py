import shutil
from secScanner.lib import *
from secScanner.gconfig import *
def S01_motd():
    InsertSection("set /etc/motd banner")

    SET_MOTD = seconf.get('basic', 'set_motd')
    MOTD = seconf.get('basic', 'motd')
    if SET_MOTD == 'yes':
        if not os.path.exists('/etc/motd_bak'):
            shutil.copy2('/etc/motd', '/etc/motd_bak')
        with open('/etc/motd', "w") as write_file:#overwrite ;if /etc/motd not exsit, this line will build a new motd
            write_file.write(MOTD)
        if os.path.exists('/etc/motd') and os.path.getsize('/etc/motd') :
            Display("- Set motd banner finished...", "FINISHED")
        else:
            Display("- Set motd banner failed...", "FAILED")
    else:
        Display("- Skip set motd banner due to config file...", "SKIPPING")



