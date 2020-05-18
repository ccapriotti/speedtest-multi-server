#!/usr/bin/env python3
#
# logs speedtest results
#

import time
import json
import speedtest
import sys
import socket
from multiprocessing.pool import Pool


def measureSpeed(singleServer):
    s.get_best_server( [singleServer] )
    s.download()
    s.upload()
    return s.results.dict()


serverPool = [3188, 23969, 12743, 6251, 24815, 24389, 28164]
startTime = time.time()
exportFile = "/mnt/nfs0/systems/speedtest.log"
fullyQualifiedServers = []
results_dict = {}

s = speedtest.Speedtest()

raw = s.get_servers( serverPool )
for d in sorted( raw.keys() ):
    fullyQualifiedServers.extend( raw[d] )

operationTime = str( int( startTime ) )


with Pool(7) as p:
    allResults = p.map(measureSpeed, fullyQualifiedServers)


totalDl = 0
totalUp = 0
timestamp = ""
pingResult = 10000

for item in allResults:
    totalDl += item["download"]
    totalUp += item["upload"]
    latestPing = item["ping"]    
    pingResult = ( latestPing if latestPing < pingResult else pingResult )
    if len(timestamp) == 0:
        timestamp = item["timestamp"].split(".")[0]

outputRecord = ",".join( [operationTime,
                          timestamp,
                          str( round( totalDl / 1024 / 1024, 2 ) ),
                          str( round( totalUp / 1024 / 1024, 2 ) ),
                          str( pingResult ),
                          str( int( time.time() - startTime ) )
                        ] )

try:
    f = open( exportFile, "a" )
except:
    print( "link-monitor: error opening file", exportFile )
    sys.exit( 255 )
f.write( outputRecord + "\n" )
f.close()

