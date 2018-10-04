"""
############################################################################

## High Altitude Balloon Club

############################################################################
"""
# Generic Modules
import time
# In House Modules
import alt_control_one_CB as alt_control		 # DONE (tentative - needs to be tested for all cases)
import log_control		 						# DONE (tested)
import gps_control		 						# DONE (tested)
# import gps_control_testLibrary as gps_control
import loiter_settings   						# TODO Madeline (need to change GPIO pin #)
import flight_variables  						# DONE
import thermocouple

if __name__ == '__main__':
	# Initialize systems
	log_control.init_log_system() 			# Logging-system setup
	gps_control.init_gps_data() 			# Ensure we are getting GPS data
	thermocouple.checkThermo()				# Make sure the thermocouple is getting reasonable data
	alt_control.init_coil_burner_system() 	# Coil-burner setup
	flight_variables.init_flags() 			# Flags for checking status

	# Start launch clocks:
	flight_variables.init_flight()

	# Begin Mission:
	while True:
		# Take data point
		log_control.take_data_point()
		# Check flags for Mission Complete / Mission Failed
		alt_control.check_status()
		# Respond to flags
		alt_control.coil_control()
		# Cycle
		time.sleep(5)
		flight_variables.missionKtr += 1
