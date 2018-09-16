"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""
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

# Define necessary functions
def init_gps_data():
    #GPS setup
	global session
	latitude = None
	subprocess.call(['sudo gpsd /dev/ttyUSB0 -n -F /var/run/gpsd.sock'], shell=True)
	print 'GPS initialized, searching for satellites...'
	print 'This might take a while...'
	time.sleep(2)
	session = gps.gps("localhost", "2947")
	session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	while isinstance(latitude, float) is False:
		time.sleep(1)
		report = session.next()
		if report['class'] == 'TPV':
			if hasattr(report, 'lat'):
				latitude = report.lat
		print 'Searching for signal...'
	print 'Signal acquired!'
	with open("systemLog.txt", "a") as logFile:
		logMsg1 = "GPS Signal Aquired Successfully\n\n"
		logFile.write(logMsg)

def timeGet():
	while True:
		try:
			report = session.next()
			if report['class'] == 'TPV':
				if hasattr(report, 'time'):
					time = report.time
					return time
				break
		except Exception as e:
			with open("systemLog.txt", "a") as logFile:
				logMsg1 = "Failed to aquire time.\n"
				logMsg2 = "Error: {}\n\n".format(e)
				logFile.write(logMsg1)
				logFile.write(logMsg2)
			return 0.0

def latGet():
	while True:
		try:
			report = session.next()
			if report['class'] == 'TPV':
				if hasattr(report, 'lat'):
					latitude = report.lat
					return latitude
				break
		except Exception as e:
			with open("systemLog.txt", "a") as logFile:
				logMsg1 = "Failed to aquire time.\n"
				logMsg2 = "Error: {}\n\n".format(e)
				logFile.write(logMsg1)
				logFile.write(logMsg2)
			return 0.0

def lonGet():
	while True:
		try:
			report = session.next()
			if report['class'] == 'TPV':
				if hasattr(report, 'lon'):
					longitude = report.lon
					return longitude
				break
		except Exception as e:
			with open("systemLog.txt", "a") as logFile:
				logMsg1 = "Failed to aquire time.\n"
				logMsg2 = "Error: {}\n\n".format(e)
				logFile.write(logMsg1)
				logFile.write(logMsg2)
			return 0.0

def altGet():
	while True:
		try:
			report = session.next()
			if report['class'] == 'TPV':
				if hasattr(report, 'alt'):
					GPSaltitude = report.alt
					return GPSaltitude
				break

		except Exception as e:
			with open("systemLog.txt", "a") as logFile:
				logMsg1 = "Failed to aquire time.\n"
				logMsg2 = "Error: {}\n\n".format(e)
				logFile.write(logMsg1)
				logFile.write(logMsg2)
			return 0.0

def climbGet():
	while True:
		try:
			report = session.next()
			if report['class'] == 'TPV':
				if hasattr(report, 'climb'):
					global climb
					climb = report.climb
					return climb
				break
		except Exception as e:
			with open("systemLog.txt", "a") as logFile:
				logMsg1 = "Failed to aquire time.\n"
				logMsg2 = "Error: {}\n\n".format(e)
				logFile.write(logMsg1)
				logFile.write(logMsg2)
			return 0.0

if __name__ == '__main__':
    init_gps_data()
