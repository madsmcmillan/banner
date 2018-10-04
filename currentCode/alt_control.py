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
import gps_control
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
    flightTime = time.time() - flight_variables.launch_start
    flightAlt = gps_control.altGet()
    # Check against kill parameters
    if flight_variables.killBalloons == 0:
        # Time exceeded before we begin to loiter?
        if (flightTime >= (loiter_settings.max_flight_time() - loiter_settings.loiter_time()) and flight_variables.cutLiftBalloon == 0):
            # Check Altitude Against Floor Altitude:
            if (flight_variables.cutLiftBalloon == 0 and
                    flightAlt >= loiter_settings.floor_altitude()):
                # We haven't reached loiter altitude yet,
                # but signal loiter anyways
                flight_variables.cutLiftBalloon = 1
                # Begin loiter clock
                global loiter_start
                loiter_start = flightTime
                with open("systemLog.txt", "a") as logFile:
                    logMsg1 = 'Signaled killBalloons at flight time: {}\n'.format(flightTime)
                    logMsg2 = 'Reason: Flight Time.\n {} vs specified {}\n'.format(flightTime, loiter_settings.max_flight_time()-loiter_settings.loiter_time())
                    logMsg3 = 'Ignoring b/c we are above floor altitude: {}\n'.format(loiter_settings.floor_altitude())
                    logMsg4 = 'Go ahead and give loiter a shot!\n\n'.format()
                    logFile.write(logMsg1)
                    logFile.write(logMsg2)
                    logFile.write(logMsg3)
                    logFile.write(logMsg4)
            else:
                # Kill Message
                flight_variables.killBalloons = 1
                with open("systemLog.txt", "a") as logFile:
                    logMsg1 = 'Signaled killBalloons at flight time: {}\n'.format(flightTime)
                    logMsg2 = 'Reason: Flight Time.\n {} vs specified {}\n\n'.format(flightTime, loiter_settings.max_flight_time())
                    logFile.write(logMsg1)
                    logFile.write(logMsg2)
        # Loitering Badly?
        elif (flight_variables.cutLiftBalloon == 2 and
                flight_variables.cutNeutralBalloon == 2):
            # We are loitering...
            # Too high!
            if flightAlt >= loiter_settings.height_limit():
                # Kill Message
                flight_variables.killBalloons = 1
                with open("systemLog.txt", "a") as logFile:
                    logMsg1 = 'Signaled killBalloons at flight time: {}\n'.format(flightTime)
                    logMsg2 = 'Reason: Max Alt.\n{} vs specified {}\n\n'.format(flightAlt, loiter_settings.height_limit())
                    logFile.write(logMsg1)
                    logFile.write(logMsg2)
            # Too low!
            elif flightAlt <= loiter_settings.floor_altitude():
                flight_variables.killBalloons = 1
                with open("systemLog.txt", "a") as logFile:
                    logMsg1 = 'Signaled killBalloons at flight time: {}\n'.format(flightTime)
                    logMsg2 = 'Reason: Min Loiter Alt.\n{} vs specified {}\n\n'.format(flightAlt, loiter_settings.floor_altitude())
                    logFile.write(logMsg1)
                    logFile.write(logMsg2)
    # Check against mission parameters
    if flight_variables.cutLiftBalloon == 0:
        if (flightAlt >= loiter_settings.loiter_alt() and
                flight_variables.killBalloons == 0):
            # Message: Jettison Lift Balloon
            flight_variables.cutLiftBalloon = 1
            # Begin loiter clock
            global loiter_start
            loiter_start = flightTime
            with open("systemLog.txt", "a") as logFile:
                logMsg = 'Signaled cutLiftBalloon at flight time: {}\n\n'.format(flightTime)
                logFile.write(logMsg)
    elif (flight_variables.cutLiftBalloon == 2 and
            flight_variables.cutNeutralBalloon == 0):
        loiterTime = flightTime - loiter_start
        if (loiterTime >= loiter_settings.loiter_time() and
                flight_variables.killBalloons == 0):
            # Message: Jettison Neutral Balloon
            flight_variables.cutNeutralBalloon = 1
            with open("systemLog.txt", "a") as logFile:
                logMsg = 'Signaled cutNeutralBalloon at flight time: {}\n\n'.format(flightTime)
                logFile.write(logMsg)


def coil_control():
    # Check flags
    if flight_variables.killBalloons == 0:
        if (flight_variables.cutLiftBalloon == 1 and
                flight_variables.cutNeutralBalloon == 0):
            # Toggle Lift
            coil_burner_1()
            flight_variables.cutLiftBalloon = 2
        elif (flight_variables.cutLiftBalloon == 2 and
                flight_variables.cutNeutralBalloon == 1):
            # Toggle Neutral
            coil_burner_2()
            flight_variables.cutNeutralBalloon = 2
            flight_variables.killBalloons = 2
    if flight_variables.killBalloons == 1:
        if (flight_variables.cutLiftBalloon == 0 and
                flight_variables.cutNeutralBalloon == 0):
            # Toggle Lift
            coil_burner_1()
            flight_variables.cutLiftBalloon = 2
            # Toggle Neutral
            coil_burner_2()
            flight_variables.cutNeutralBalloon = 2
        elif (flight_variables.cutLiftBalloon == 2 and
                flight_variables.cutNeutralBalloon == 0):
            # Toggle Neutral
            coil_burner_2()
            flight_variables.cutNeutralBalloon = 2


def coil_burner_1():
    # Turn on coil_burner_1
    GPIO.output(loiter_settings.coil_value_1(), GPIO.HIGH)  # Cut Lift Balloon
    time.sleep(loiter_settings.burn_time())
    GPIO.output(loiter_settings.coil_value_1(), GPIO.LOW)


def coil_burner_2():
    GPIO.output(loiter_settings.coil_value_2(), GPIO.HIGH)  # Cut Lift Balloon
    time.sleep(loiter_settings.burn_time())
    GPIO.output(loiter_settings.coil_value_2(), GPIO.LOW)
