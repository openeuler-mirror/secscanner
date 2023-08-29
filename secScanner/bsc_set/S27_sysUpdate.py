from secScanner.lib import *
def S29_sysUpdate():
    logger = logging.getLogger("secscanner")
    InsertSection("Update system...")
    logger.info("BSE will not update system automatically, use 'yum update' by yourself.")
    Display(f"- BSE will not do this, do it by yourself if you want...", "SKIPPING")
