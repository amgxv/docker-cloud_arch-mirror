#!/usr/bin/python

from ping3 import ping
from urllib.parse import urlsplit
import os
import subprocess
import threading
import logging
import bestmirror
import time
import psutil
import check_update as ch_up

# Log Format
logformat = '%(asctime)s - %(levelname)s - %(name)s - %(message)s' 
logging.basicConfig(level=logging.INFO, format=logformat)
logger = logging.getLogger(__name__)

# Refresh Time
refresh = 5.0

def fetch_mirror():

    t = threading.Timer(refresh, fetch_mirror)
    t.start()

    #TODO: If rsync is still don't do nothing
            
    mirror_file="./mirrors"
    if os.path.isfile(mirror_file) == False:
        logger.error("Mirror file not detected...")
        bestmirror.get_best_mirrors()

    # Get mirrors from textfile and it starts rsync if ping goes well
    f = open(mirror_file,'r')
    
    try:
        for mirror in f:
            mirror = mirror.replace("\n", "")
            url = mirror
            base_url = "{0.netloc}".format(urlsplit(url))
            p = ping(base_url, unit='ms')

            if p is None:
                logger.warn("Error fetching mirror {mirror}".format(mirror=mirror))
                pass

            if p is not None:
                if ch_up.checkUpdate(mirror) is True:
                    logger.info("Fetching latest packages from : {mirror}".format(mirror=mirror))
                    subprocess.run("rsync -rtlvH --delete-after --delay-updates --safe-links {mirror}/iso {path}".format(mirror=mirror, path="./mirror"), shell=True)
                    logger.info("Mirror updated successfully!")
                    break
                else:
                    pass
    
    except:
        logger.error("Error fetching from mirrors :c")

    f.close()

if __name__ == "__main__":    
    fetch_mirror()
