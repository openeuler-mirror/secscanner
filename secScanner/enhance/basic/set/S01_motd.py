import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S01_motd():
    InsertSection("set /etc/motd banner")
    set_motd = seconf.get('basic', 'set_motd')
    motd = seconf.get('basic', 'motd')
    if set_motd == 'yes':
        if os.path.exists('/etc/motd') and not os.path.exists('/etc/motd_bak'):
            shutil.copy2('/etc/motd', '/etc/motd_bak')
        if not os.path.exists('/etc/motd'):
            pathlib.Path('/etc/motd').touch()
            os.chmod('/etc/motd', 600)
        if os.path.exists('/etc/motd'):
            with open('/etc/motd', "w") as write_file:
                write_file.write(motd)
            if os.path.getsize('/etc/motd'):
                logger.info("set the motd banner successfully")
                Display("- Set motd banner finished...", "FINISHED")
    else:
        Display("- Skip set motd banner due to config file...", "SKIPPING")



