"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""

# Pin number on the RPi pinout diagram is different from the GPIO port number


# All flight settings
def loiter_alt():
    value = 15240  # 15,240 m = 50,000 ft
    return value


def loiter_time():
    value = 1200  # Loiter time before flight termination (seconds)
    return value


def delta_accel():
    value = 6  # threshold of change in acceleration indicating balloon severance
    return value


def burn_time():
    value = 6  # seconds that the coil burners are on
    return value


# All kill settings
def height_limit():
    value = 19812  # 19,812 m = 65,000 ft
    return value


def max_flight_time():
    value = 3600  # 3600 s = 1 hr
    return value


def floor_altitude():
    value = 12192  # 12,192 m = 40,000 ft
    return value


# All relay control pins
def coil_value_1():
    value = 8  # pin 18, gpio 24
    return value


def coil_value_2():
    value = 10  # pin 12, gpio 18
    return value


def solenoid_valve():
    value = 12  # pin 12, gpio 18
    return value
