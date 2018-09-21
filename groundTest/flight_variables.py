"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""
# Generic Modules
import time
# In House Modules


def init_flight():
    # Initialize launch clock:
    global launch_start
    launch_start = time.time()
    # Initialize Mission Ktr (May not be used):
    global missionKtr
    missionKtr = 0


def init_flags():
    # Initialize Global Variables
    # Set First Values: ALL ZEROS
    global cutLiftBalloon
    cutLiftBalloon = 0
    global cutNeutralBalloon
    cutNeutralBalloon = 0
    global killBalloons
    killBalloons = 0


def init_loiter():
    # Initialize loiter clock:
    global loiter_start
    loiter_start = time.time()
