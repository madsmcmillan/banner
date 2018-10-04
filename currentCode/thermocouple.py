##############################################################################

# Project Banner: thermocouple readings via AD8495 & ADS1015
# Created: 7-11-16 by Madeline McMillan and Nate Peirson
# Texas A&M University, Department of Aerospace Engineering
# High Altitude Balloon Club

# This converts analog signal to digital using Adafruit_ADS1x15 ADC
# and library, then maths to get temperature

##############################################################################

import Adafruit_ADS1x15

# Gain to voltage ranges. If you change the gain, change the voltage
# in the thermocouple amplifier mathematics!
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V


def checkThermo():
    adc = Adafruit_ADS1x15.ADS1015()
    global GAIN
    GAIN = 1
    value = (((float(adc.read_adc(0, gain=GAIN)) / 2048.0) * 4.096) - 1.25) / 0.005
    if value < 300:
        print('Thermocouple good!\n')  # terminal feedback
        with open("systemLog.txt", "a") as logFile:
            logMsg1 = "GPS Signal Aquired Successfully\n\n"
            logFile.write(logMsg1)


def readThermo():
    adc = Adafruit_ADS1x15.ADS1015()
    while True:
        try:
            value = (((float(adc.read_adc(0, gain=GAIN)) / 2048.0) * 4.096) - 1.25) / 0.005
            return(value)  # for external applications
        except Exception as e:
            with open("systemLog.txt", "a") as logFile:
                logMsg1 = "Failed to aquire temperature data.\n"
                logMsg2 = "Error: {}\n\n".format(e)
                logFile.write(logMsg1)
                logFile.write(logMsg2)
            return 0.0


if __name__ == '__main__':
    print('-----------------------\nReading thermocouple...\n-----------------------')
    checkThermo()
    value = readThermo
    print(value)  # for independent sampling in terminal
