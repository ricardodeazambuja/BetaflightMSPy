"""example.py: Just an example of how to use YAMSPy.

Copyright (C) 2019 Ricardo de Azambuja

This file is part of YAMSPy.

YAMSPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YAMSPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YAMSPy.  If not, see <https://www.gnu.org/licenses/>.

Acknowledgement:
This work was possible thanks to the financial support from IVADO.ca (postdoctoral scholarship 2019/2020).

Disclaimer (adapted from Wikipedia):
None of the authors, contributors, supervisors, administrators, employers, friends, family, vandals, or anyone else 
connected (or not) with this project, in any way whatsoever, can be made responsible for your use of the information (code) 
contained or linked from here.
"""

import sys
import serial

from yamspy import MSPy

"""Usage example... and testing ;)
"""
command_list = []

command_list.append([['MSP_RAW_IMU', 'MSP_ATTITUDE', 'MSP_ALTITUDE', 'MSP_SONAR', 'MSP_DEBUG'], 'SENSOR_DATA'])
command_list.append([['MSP_RAW_GPS', 'MSP_COMP_GPS', 'MSP_GPS_SV_INFO'], 'GPS_DATA'])
command_list.append([['MSP_MOTOR'], 'MOTOR_DATA'])
command_list.append([['MSP_RC'], 'RC'])
command_list.append([['MSP_ANALOG'], 'ANALOG'])
command_list.append([['MSP_VOLTAGE_METERS'], 'VOLTAGE_METERS'])
command_list.append([['MSP_CURRENT_METERS'], 'CURRENT_METERS'])
command_list.append([['MSP_BATTERY_STATE'], 'BATTERY_STATE'])
command_list.append([['MSP_SENSOR_ALIGNMENT'], 'SENSOR_ALIGNMENT'])
command_list.append([['MSP_BOARD_ALIGNMENT_CONFIG'], 'BOARD_ALIGNMENT_CONFIG'])
command_list.append([['MSP_ARMING_CONFIG'], 'ARMING_CONFIG'])
command_list.append([['MSP_FEATURE_CONFIG'], 'FEATURE_CONFIG'])
command_list.append([['MSP_RX_CONFIG'], 'RX_CONFIG'])
command_list.append([['MSP_RX_MAP'], 'RC_MAP'])
command_list.append([['MSP_MODE_RANGES'], 'MODE_RANGES'])
command_list.append([['MSP_MODE_RANGES_EXTRA'], 'MODE_RANGES_EXTRA'])
command_list.append([['MSP_ADJUSTMENT_RANGES'], 'ADJUSTMENT_RANGES'])
command_list.append([['MSP_RXFAIL_CONFIG'], 'RXFAIL_CONFIG'])
command_list.append([['MSP_FAILSAFE_CONFIG'], 'FAILSAFE_CONFIG'])
command_list.append([['MSP_VOLTAGE_METER_CONFIG'], 'VOLTAGE_METER_CONFIGS'])
command_list.append([['MSP_CURRENT_METER_CONFIG'], 'CURRENT_METER_CONFIGS'])
command_list.append([['MSP_BATTERY_CONFIG'], 'BATTERY_CONFIG'])
command_list.append([['MSP_RC_TUNING'], 'RC_TUNING'])
command_list.append([['MSP_PID'], 'PIDs'])
command_list.append([['MSP_LOOP_TIME'], 'FC_CONFIG'])
command_list.append([['MSP_MISC'], 'MISC'])
command_list.append([['MSP_MOTOR_CONFIG'], 'MOTOR_CONFIG'])
command_list.append([['MSP_COMPASS_CONFIG'], 'COMPASS_CONFIG'])
command_list.append([['MSP_GPS_CONFIG'], 'GPS_CONFIG'])
command_list.append([['MSP_GPS_RESCUE'], 'GPS_RESCUE'])
command_list.append([['MSP_RSSI_CONFIG'], 'RSSI_CONFIG'])
command_list.append([['MSP_MOTOR_3D_CONFIG'], 'MOTOR_3D_CONFIG'])
command_list.append([['MSP_BOXNAMES'], 'AUX_CONFIG'])
command_list.append([['MSP_BOXIDS'], 'AUX_CONFIG_IDS'])
command_list.append([['MSP_PIDNAMES'], 'PIDNAMES'])
command_list.append([['MSP_SERVO_CONFIGURATIONS'], 'SERVO_CONFIG'])
command_list.append([['MSP_RC_DEADBAND'], 'RC_DEADBAND_CONFIG'])
command_list.append([['MSP_BEEPER_CONFIG'], 'BEEPER_CONFIG'])
command_list.append([['MSP_MIXER_CONFIG'], 'MIXER_CONFIG'])
command_list.append([['MSP_CF_SERIAL_CONFIG'], 'SERIAL_CONFIG'])
command_list.append([['MSP_ADVANCED_CONFIG'], 'PID_ADVANCED_CONFIG'])
command_list.append([['MSP_FILTER_CONFIG'], 'FILTER_CONFIG'])
command_list.append([['MSP_PID_ADVANCED'], 'ADVANCED_TUNING'])
command_list.append([['MSP_SENSOR_CONFIG'], 'SENSOR_CONFIG'])
command_list.append([['MSP_DATAFLASH_SUMMARY'], 'DATAFLASH'])
command_list.append([['MSP_SDCARD_SUMMARY'], 'SDCARD'])
command_list.append([['MSP_BLACKBOX_CONFIG'], 'BLACKBOX'])
command_list.append([['MSP_TRANSPONDER_CONFIG'], 'TRANSPONDER'])
command_list.append([['MSP_PID_CONTROLLER'], 'PID'])

with MSPy(device="/dev/ttyACM0") as board:
    if board==1:
        print("An error ocurred... probably the serial port is not available ;)")
        sys.exit(1)

    #
    # The commands bellow will list / test all the possible messages implemented here:
    #
    for msg_list, sto_loc in command_list: 
        print("\nINITIAL {}:".format(sto_loc))
        print(getattr(board, sto_loc))
        for msg in msg_list:
            if board.send_RAW_msg(MSPy.MSPCodes[msg], data=[]):
                print('{} requested!'.format(msg))
                dataHandler = board.receive_msg()
                board.process_recv_data(dataHandler)

        print("\nFINAL {}:".format(sto_loc))
        print(getattr(board, sto_loc))

    print("armingDisableFlags: {}".format(board.process_armingDisableFlags(board.CONFIG['armingDisableFlags'])))

    if board.reboot():
        try:
            dataHandler = board.receive_msg()
            board.process_recv_data(dataHandler)
        except serial.SerialException:
            print("Board is rebooting")