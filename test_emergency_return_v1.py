

import pytest
from conftest import *
import time
import threading
import logging
#import drone from conftest
CRITICAL_BATTERY_THRESHOLD  = 0.20
TIMEOUT_EMERGENCY_RETURN    = 60
HOME                        =(48.1351, 11.5820, 0.0)
MAX_WIND_SPEED              =35
RTH_TIMEOUT_S               = 60.0   # max seconds to wait for drone to reach HOME after RTH

TEST_CASE_ID="TC-E-005-EXT"

class DroneSetupError(RuntimeError):
    """Raised when drone initialisation steps fail."""

class Drone_Preconditions:
  def case_check_intial_battery_status(self,drone,log):
     
        
            assert drone.battery_level>=CRITICAL_BATTERY_THRESHOLD ,f"Low Battery Test Case does not fit the preconditions {drone.battery_level}"
            log.info(f"{TEST_CASE_ID} Precondition Initial Battery Checked. {drone.battery_level}")
      
            assert drone.position==HOME,"HOME location not set,Test Case does not fit the preconditions "
            log.info("{TEST_CASE_ID} Precondition Location Check.")
        
        
       
            assert drone.distance==0,"Distance Not set to zero"
            log.info("{TEST_CASE_ID} Precondition Distance Checked.")
            
        
            assert drone.wind<=MAX_WIND_SPEED,f"Wind Speed is greater than {MAX_WIND_SPEED}" 
            log.info("{TEST_CASE_ID} Precondition windspeed Checked.")
  
       
            
        
   


class TestEmergencyReturn():
    
    def test_TC_E_005_EXT(self,drone,log):
      
            pre_conditions=Drone_Preconditions()
            pre_conditions.case_check_intial_battery_status(drone,log)
            deadline = time.monotonic() + RTH_TIMEOUT_S
            try:
                #test steps power on drone
                drone.power_on_drone()
                log.info(f"{TEST_CASE_ID} Drone Power On.")
  
                #enable GPS
                drone.gps_lock()
                log.info(f"{TEST_CASE_ID} GPS Locked with more than 6 satellites.")
                #Change to mission mode
                drone.set_position(HOME)
                log.info(f"{TEST_CASE_ID} Home Position Set Enabled.")
                drone.start_mission()
                log.info(f"{TEST_CASE_ID} Moving to Target Mission Enabled.")
                drone.simulate_battery_drain_to(10)
            except Exception as error:
                log.error(f"{TEST_CASE_ID} Precondition windspeed Checked.")
                raise DroneSetupError(f"Drone initialisation failed {error}")    

          
            
            assert drone.mode==Mode.RTH,(
                f"Mode mismatch — expected {Mode.RTH}, got '{drone.mode}'. "
                f"Battery: {drone.battery:.1%}")
            log.info(f"{TEST_CASE_ID} Drone Mode Set to {drone.mode} Sucessfullyat battery level {drone.battery_level}")

            drone.update_simulation()
            
            assert drone.mode==Mode.LANDED,"Failed Drone Landing"
            log.info("{TEST_CASE_ID} Drone Landed Sucessfully.")
            assert drone.position==HOME,"Failed to Come to Home Position"
            log.info("{TEST_CASE_ID} Drone Position Verified Sucessfully.")
       


  
       

