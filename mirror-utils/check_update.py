import os
import hashlib
import threading
import logging
import fetch_mirror as fm

# Paths to lastupdate file
checkdir = './.check/'
mirrordir = './mirror/'
lastupdate_file = f"{checkdir}lastupdate"
local_lastupdate_file = f'{mirrordir}lastupdate'


# Log Format
logformat = '%(asctime)s - %(levelname)s - %(name)s - %(message)s' 
logging.basicConfig(level=logging.INFO, format=logformat)
logger = logging.getLogger(__name__)


def checkUpdate(mirror):
    
    if not os.path.isdir(checkdir):
        os.makedirs(checkdir)
    
    if not os.path.isdir(mirrordir):
        os.makedirs(mirrordir)

    if not os.path.isfile(lastupdate_file):
        logger.warn("Last update file not found, creating one...")
        file = open(lastupdate_file, "w")
        file.write("INITIAL")
        file.close()

    if not os.path.isfile(local_lastupdate_file):
        logger.warn("Local mirror last update file not found, creating one...")
        file = open(local_lastupdate_file, "w")
        file.write("0000000")
        file.close()

    # Get lastupdate file from remote Tier1 mirror
    get_last_update = os.system(f"rsync -qt {mirror} {lastupdate_file}")

    # Read hash from local and remote file
    localmd5 = hashlib.md5(open(local_lastupdate_file,'rb').read()).hexdigest()
    remotemd5 = hashlib.md5(open(lastupdate_file,'rb').read()).hexdigest()

    if localmd5 != remotemd5:
        logger.info(f"Local checksum : {localmd5}")
        logger.info(f"Remote checksum : {remotemd5}")
        logger.info("Checksums are not equal, updating mirror...")
        return True
    else:
        logger.info("Mirror is up to date")
        return False

if __name__ == "__main__":
    checkUpdate()
