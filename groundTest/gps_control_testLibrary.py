"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""
# FOR TESTING PURPOSES ONLY
# ---Function Library---
# Initialize:   init_gps_data()
#       Time:   timeGet()
#   Latitude:   latGet()
#  Longitude:   lonGet()
#   Altitude:   altGet()
#  Climb/ROA:   climbGet()

# Import necessary modules
import gps
import time
import subprocess
# In house modules
import flight_variables

# Define necessary functions
def init_gps_data():
    #GPS setup
    with open("systemLog.txt", "a") as logFile:
        logMsg1 = 'Assuming GPS Signal Acquired Successfully\n\n'
        logFile.write(logMsg1)
    # Open and save test data
    with open("slowLaunchData.txt", "r") as dataFile:
        dlines = []
        for line in dataFile:
            dlines.append(line.rstrip('\n'))
    testDataTime = []
    testDataAlt  = []
    for i in range(0,len(dlines)):
        testDataTime.append(dlines[i].split( )[0])
        testDataAlt.append(dlines[i].split( )[1])
    global testTime
    testTime = testDataTime
    global testAlt
    testAlt = testDataAlt

def timeGet():
    try:
        return float(testTime[flight_variables.missionKtr])
    except:
        return 0.0

def latGet():
	return 100.0

def lonGet():
	return 100.0

def altGet():
	return float(testAlt[flight_variables.missionKtr])

def climbGet():
	return 1.0

if __name__ == '__main__':
    init_gps_data()
