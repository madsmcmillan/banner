"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""
# -------Function Library-------
# Begin Launch Files: init_log_system
#    Take Data Point: take_data_point

# Import necessary modules
# Generic Modules
import time
# In House modules
#import gps_control
import gps_control_testLibrary as gps_control

# Define necessary functions

def init_log_system():
    # Write beginning of system log
    with open("systemLog.txt", "w") as logFile:
        logFile.write("System Messages.\n")
        logFile.write("----------------\n\n")

    # Write beginning of data log
    with open("dataLog.txt", "w") as dataFile:
        dataFile.write("Flight Data Log\n")
        dataFile.write("Mission Start Time: ")
        dataFile.write(str(gps_control.timeGet()))
        dataFile.write("\n----------------------------------")
        dataFile.write("\n\nTimestamp\tAltitude (m)\tLatitude\tLongitude\tClimb (m/Min)\n")

def take_data_point():
    flightAlt  = gps_control.altGet()
    flightTime = time.time() - flight_variables.launch_start
    flightLong = gps_control.lonGet()
    flightLat  = gps_control.latGet()
    flightClimb = gps_control.climbGet()
    dataMessage = '{} \t {} \t {} \t {} \t {} \n'.format(str(flightTime), str(flightAlt), str(flightLat), str(flightLong), str(flightClimb))
    with open("dataLog.txt", "a") as dataFile:
        dataFile.write(dataMessage)

# Testing this Module
if __name__ == '__main__':
    gps_control.init_gps_data()
    init_log_system()
    time.sleep(3)
    with open("systemLog.txt", "a") as logFile:
        logFile.write("Testing the system...\n")
    take_data_point()
