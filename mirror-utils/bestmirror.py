#!/usr/bin/python

from ping3 import ping, verbose_ping
import json
import requests
import statistics
from urllib.parse import urlsplit

def get_best_mirrors():
    # Get all working tier 1 mirrors
    r = requests.get("https://www.archlinux.org/mirrors/status/tier/1/json/")
    cont = json.loads(r.text)
    mirror_list = []
    for mirror in cont['urls']:
        mirror_list.append(mirror['url'])

    # Filter by rsync mirrors
    rsync_mirrors = []
    for mirror in mirror_list:
        if 'rsync' in mirror:
            rsync_mirrors.append(mirror)

    # Ping mirrors to get the closer and stable mirror
    print ("Pinging mirrors...")
    ping_results = []
    for mirror in rsync_mirrors:
        url = mirror
        base_url = "{0.netloc}".format(urlsplit(url))
        # Make 5 pings (or 1 if first cannot be done)...
        q = [ping(base_url, unit='ms')]
        q += [ping(base_url, unit='ms') for _ in range(0, 4)] if q[0] is not None else []
        # ...delete the None values
        r = [x for x in q if x is not None]
        # ...get the mean if list is not empy
        p = statistics.mean(r) if len(r) > 0 else None

        if p is None:
            pass
        else:
            rounded = round((p),2)
            ping_result = tuple([mirror, rounded])
            ping_results.append(ping_result)

    elements = len(ping_results)
    sorted_mirrors = sorted([ping_results[x][0] for x in range(0,elements)])
    limit = [sorted_mirrors[x] for x in range(0,5)]

    # Write closest mirrors to a textfile
    f = open('./mirrors.txt','w')
    for mirror in limit:
        f.write(f'{mirror}\n')

if __name__ == "__main__":
    get_best_mirrors()
