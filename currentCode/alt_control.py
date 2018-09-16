"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""
# ---Function Library---
# Initialize System: init_coil_burner_system
# Check Alt. Status: check_status
#     Control Coils: coil_control
#         Cycle CB1: coil_burner_1
#         Cycle CB2: coil_burner_2

# Import necessary modules
# Generic Modules
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
# In House Modules
#import gps_control
import gps_control_testLibrary as gps_control
import loiter_settings
import flight_variables

# Define necessary functions
def init_coil_burner_system():
    # Set up GPIO pins
    try:
        GPIO.setup(loiter_settings.coil_value_1(), GPIO.OUT)
        GPIO.setup(loiter_settings.coil_value_2(), GPIO.OUT)
    except Exception as e:
        with open("systemLog.txt", "a") as logFile:
            logMsg1 = "Failed to initialize coil burners.\n"
            logMsg2 = "Error: {}\n\n".format(e)
            logFile.write(logMsg1)
            logFile.write(logMsg2)

def check_status():
    # Get Stats:
    flightTime = time.time() - launch_start
    flightTime = gps_control.timeGet()
    # Check against mission parameters
    if flightAlt >= loiter_settings.loiter_alt() and flight_variables.cutLiftBalloon == 0 and flight_variables.killBalloons == 0:
        # Message: Jettison Lift Balloon
        flight_variables.cutLiftBalloon = 1
        with open("systemLog.txt","a") as logFile:
            logMsg = 'Signaled cutLiftBalloon at flight time: {}\n\n'.format(flightTime)
            logFile.write(logMsg)
    elif loiterTime >= loiter_settings.loiter_time() and flight_variables.cutNeutralBalloon == 0 and flight_variables.killBalloons == 0:
        # Message: Jettison Neutral Balloon
        flight_variables.cutNeutralBalloon = 1
        with open("systemLog.txt","a") as logFile:
            logMsg = 'Signaled cutNeutralBalloon at flight time: {}\n\n'.format(flightTime)
            logFile.write(logMsg)
    # Check against kill parameters
    if flightAlt >= loiter_settings.height_limit() and flight_variables.killBalloons == 0:
        # Kill Message
        flight_variables.killBalloons = 1
        with open("systemLog.txt","a") as logFile:
            logMsg1 = 'Signaled killBalloons at flight time: {}\n'.format(flightTime)
            logMsg2 = 'Reason: Max Alt.\n{} vs specified {}\n\n'.format(flightAlt,loiter_settings.height_limit())
            logFile.write(logMsg1)
            logFile.write(logMsg2)
    elif flightTime >= loiter_settings.max_flight_time() and flight_variables.killBalloons == 0:
        # Kill Message
        flight_variables.killBalloons = 1
        with open("systemLog.txt","a") as logFile:
            logMsg1 = 'Signaled killBalloons at flight time: {}\n'.format(flightTime)
            logMsg2 = 'Reason: Flight Time.\n{} vs specified {}\n\n'.format(flightTime,loiter_settings.max_flight_time())
            logFile.write(logMsg1)
            logFile.write(logMsg2)

def coil_control():
    # Check flags
    if flight_variables.killBalloons == 1:
        # Terminate Mission
        # Check if any coil burners have already been activated
        if flight_variables.CB1_Burned == 1 and flight_variables.CB2_Burned == 1:
            # Something may be wrong. Should be ending mission currently
            with open("systemLog.txt", "a") as logFile:
                logMsg1 = 'killBalloons signaled, but both coil burners show release.\n'
                logMsg2 = 'Doing nothing. \n\n'
                logFile.write(logMsg1)
                logFile.write(logMsg2)
        elif flight_variables.CB1_Burned == 1 and flight_variables.CB2_Burned == 0:
            # Lift balloon released, but not neutral Balloon
            # Activate CB2
            coil_burner_2()
            with open("systemLog.txt", "a") as logFile:
                logMsg1 = 'killBalloon signaled, cutting neutral balloon.\n\n'
                logFile.write(logMsg1)
        elif flight_variables.CB1_Burned == 0 and flight_variables.CB2_Burned == 1:
            # ??? Neutral balloon shows released, and lift balloon shows attached.
            # Activate CB1
            coil_burner_1()
            with open("systemLog.txt", "a") as logFile:
                logMsg1 = 'Balloons backwards???\n\n'
                logFile.write(logMsg1)
        elif flight_variables.CB1_Burned == 0 and flight_variables.CB2_Burned == 0:
            # Neither burner has gone off yet.
            coil_burner_1()
            coil_burner_2()
            with open("systemLog.txt", "a") as logFile:
                logMsg1 = 'killBalloons signaled, Both coil burners activated.\n\n'
                logFile.write(logMsg1)
    elif flight_variables.cutLiftBalloon == 1:
        if flight_variables.CB1_Burned == 1:
            # Already cut the balloon
            pass
        else:
            # Cut the lift balloon.
            coil_burner_1()
            flight_variables.CB1_Burned = 1
            # begin loiter counter
            flight_variables.loiter_start = time.time()
    elif flight_variables.cutNeutralBalloon == 1:
        if flight_variables.CB2_Burned == 1:
            # Already cut the balloon
            pass
        else:
            # Cut the neutral balloon.
            coil_burner_2()
            flight_variables.CB2_Burned = 1

def coil_burner_1():
    # Turn on coil_burner_1
    GPIO.output(loiter_settings.coil_value_1(), GPIO.HIGH) # Cut Lift Balloon
    time.sleep(loiter_settings.burn_time())
    GPIO.output(loiter_settings.coil_value_1(), GPIO.LOW)

def coil_burner_2():
    GPIO.output(loiter_settings.coil_value_2(), GPIO.HIGH) # Cut Lift Balloon
    time.sleep(loiter_settings.burn_time())
    GPIO.output(loiter_settings.coil_value_2(), GPIO.LOW)
