# convert the raw logs from Bowie the robot to a .csv file
# usage: python convert_data.py <<input dir>> <<output file.csv>>
#
# by Erin RobotGrrl for Robot Missions
# robotmissions.org
# Written August 13, 2016
# Updated June 7, 2018 - Revised parsing with unicode decode
#                        errors, and added more sensors
# Updated October 12, 2018

import sys
import os

# change your current robot (or logging profile) here
# 0 = OG Bowie
# 1 = Yellow Bowie
# 2 = time, gps, temperature, altitude
LOGGING_PROFILE = 2


#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print("The arguments are: " , str(sys.argv))

if len(sys.argv) >= 1:
    DIR = sys.argv[1]
else:
    print("Please specify a directory")
    exit()

list_dir = os.listdir(DIR)

NUM_LOGS = 0
for root, dirs, files in os.walk(DIR):  
    for filename in files:
        if filename.startswith("LOG"):
            NUM_LOGS += 1

savename = DIR + "/" + "environmental_log.csv"
apisavename = DIR + "/" + "api_log.csv"
autonsavename = DIR + "/" + "auton_log.csv"

if len(sys.argv) >= 3:
    savename = DIR + "/" + sys.argv[2]
    apisavename = DIR + "/" + sys.argv[3]
    autonsavename = DIR + "/" + sys.argv[4]

outfile = open(savename, 'w')
apioutfile = open(apisavename, 'w')
autonoutfile = open(autonsavename, 'w')
total_log_lines = 0
api_event_count = 0
auton_event_count = 0
num_unicode_errors = 0
urad_ind_start = 33 # the index that the uradmonitor data starts on


LOG_TIME = True
LOG_MOTOR_A_SPEED = True
LOG_MOTOR_A_DIR = True
LOG_MOTOR_B_SPEED = True
LOG_MOTOR_B_DIR = True
LOG_MOTOR_CURRENT = True
LOG_SERVO_POS_ARM_L = True
LOG_SERVO_POS_ARM_R = True
LOG_SERVO_POS_END = True
LOG_SERVO_POS_HOPPER = True
LOG_SERVO_POS_LID = True
LOG_SERVO_POS_EXTRA = True
LOG_SERVO_CURRENT = True
LOG_LED_FRONT_L = True
LOG_LED_FRONT_R = True
LOG_LED_BACK_L = True
LOG_LED_BACK_R = True
LOG_IMU_PITCH = True
LOG_IMU_ROLL = True
LOG_IMU_YAW = True
LOG_COMPASS_HEADING = True
LOG_GPS_SATS = True
LOG_GPS_HDOP = True
LOG_GPS_LATITUDE = True
LOG_GPS_LONGITUDE = True
LOG_GPS_ALTITUDE = True
LOG_BATTERY = True
LOG_COMM_XBEE_LATENCY = True
LOG_COMM_ARDUINO_LATENCY = True
LOG_HUMIDITY = True
LOG_TEMPERATURE = True
LOG_UV = True
LOG_WIND = True
LOG_URADMONITOR = True # FUTURE: might want to break this down to individual sensors


# turn off what isn't needed in the environmental log here
if LOGGING_PROFILE == 0: #OG BOWIE

    LOG_TIME = True

elif LOGGING_PROFILE == 1: # YELLOW BOWIE

    LOG_UV = False
    LOG_WIND = False
    LOG_URADMONITOR = False

elif LOGGING_PROFILE == 2: # time, gps, temperature, altitude

    LOG_MOTOR_A_SPEED = False
    LOG_MOTOR_A_DIR = False
    LOG_MOTOR_B_SPEED = False
    LOG_MOTOR_B_DIR = False
    LOG_MOTOR_CURRENT = False
    LOG_SERVO_POS_ARM_L = False
    LOG_SERVO_POS_ARM_R = False
    LOG_SERVO_POS_END = False
    LOG_SERVO_POS_HOPPER = False
    LOG_SERVO_POS_LID = False
    LOG_SERVO_POS_EXTRA = False
    LOG_SERVO_CURRENT = False
    LOG_LED_FRONT_L = False
    LOG_LED_FRONT_R = False
    LOG_LED_BACK_L = False
    LOG_LED_BACK_R = False
    LOG_IMU_PITCH = False
    LOG_IMU_ROLL = False
    LOG_IMU_YAW = False
    LOG_COMPASS_HEADING = False
    LOG_GPS_SATS = False
    LOG_GPS_HDOP = False
    LOG_BATTERY = False
    LOG_COMM_XBEE_LATENCY = False
    LOG_COMM_ARDUINO_LATENCY = False
    LOG_HUMIDITY = False
    LOG_UV = False
    LOG_WIND = False
    LOG_URADMONITOR = False




def checkToIncludeThisItem(point_index):

    if LOG_TIME == True and point_index == 0:
        return True

    if LOG_MOTOR_A_SPEED == True and point_index == 1:
        return True

    if LOG_MOTOR_A_DIR == True and point_index == 2:
        return True

    if LOG_MOTOR_B_SPEED == True and point_index == 3:
        return True

    if LOG_MOTOR_B_DIR == True and point_index == 4:
        return True

    if LOG_MOTOR_CURRENT == True and point_index == 5:
        return True

    if LOG_SERVO_POS_ARM_L == True and point_index == 6:
        return True

    if LOG_SERVO_POS_ARM_R == True and point_index == 7:
        return True

    if LOG_SERVO_POS_END == True and point_index == 8:
        return True

    if LOG_SERVO_POS_HOPPER == True and point_index == 9:
        return True

    if LOG_SERVO_POS_LID == True and point_index == 10:
        return True

    if LOG_SERVO_POS_EXTRA == True and point_index == 11:
        return True

    if LOG_SERVO_CURRENT == True and point_index == 12:
        return True

    if LOG_LED_FRONT_L == True and point_index == 13:
        return True

    if LOG_LED_FRONT_R == True and point_index == 14:
        return True

    if LOG_LED_BACK_L == True and point_index == 15:
        return True

    if LOG_LED_BACK_R == True and point_index == 16:
        return True

    if LOG_IMU_PITCH == True and point_index == 17:
        return True

    if LOG_IMU_ROLL == True and point_index == 18:
        return True

    if LOG_IMU_YAW == True and point_index == 19:
        return True

    if LOG_COMPASS_HEADING == True and point_index == 20:
        return True

    if LOG_GPS_SATS == True and point_index == 21:
        return True

    if LOG_GPS_HDOP == True and point_index == 22:
        return True

    if LOG_GPS_LATITUDE == True and point_index == 23:
        return True

    if LOG_GPS_LONGITUDE == True and point_index == 24:
        return True

    if LOG_GPS_ALTITUDE == True and point_index == 25:
        return True

    if LOG_BATTERY == True and point_index == 26:
        return True

    if LOG_COMM_XBEE_LATENCY == True and point_index == 27:
        return True

    if LOG_COMM_ARDUINO_LATENCY == True and point_index == 28:
        return True

    if LOG_HUMIDITY == True and point_index == 29:
        return True

    if LOG_TEMPERATURE == True and point_index == 30:
        return True

    if LOG_UV == True and point_index == 31:
        return True

    if LOG_WIND == True and point_index == 32:
        return True

    if LOG_URADMONITOR == True and point_index >= 33:
        return True

    return False









for log_count in range(0, NUM_LOGS): # go through each of the log files

    total_filename = DIR + "/LOG_" + str(log_count) + ".csv"
    f = open(total_filename, 'r')
    
    # TODO: This has to be updated with printing the proper
    # headers according to the logging profile
    if log_count == 0:
        s1 = f.readline()
        s1 = s1[:-1]
        s1 += ",pm 2.5,pm 10,O2,NO2,SO2,NH3" # adding these to the headers
        #print(s1)
        outfile.write("%s\n" % (s1))
        linenum = 1
        total_log_lines = total_log_lines+1

        f.close()
    
    # count the number of lines in advance in case of the decode error
    # done this way to avoid crashing on this error
    f = open(total_filename, 'r')
    counting_lines = True
    number_of_lines = 0
    while counting_lines == True:
        try:
            woo = f.readline()
            if woo == '':
                counting_lines = False
                break
        except UnicodeDecodeError:
            print("ok")
        except EOFError:
            print("end of file")
            counting_lines = False
            break
        number_of_lines += 1
    print("Number of lines = ", number_of_lines)
    f.close()

    f = open(total_filename, 'r', encoding="utf-8")
    try:
        s1 = f.readline() # skip the first one, already read it previously
    except UnicodeDecodeError:
        print("!!! A UnicodeDecodeError has occured on this line:");
        print(s)
        print("We will skip it")
        num_unicode_errors += 1
        continue

    for k in range(0, number_of_lines):
        
        # sometimes receive this error
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x9e in position 557: invalid start byte
        try:
            s = f.readline()
        except UnicodeDecodeError:
            print("!!! A UnicodeDecodeError has occured on this line:");
            print(s)
            print("We will skip it")
            num_unicode_errors += 1
            continue
        
        splittystring = s.split(",")
        
        datum = []
        for i in range(0, urad_ind_start+6+1): #todo: will this cause an error for the api event lines?
            datum.append(0)
        append_count = 0
        for item in splittystring:
            if item == ' ' or item == '' or item == '\n':
                1+1 # we'll skip writing this line to the file
                skippy = True
            else:
                datum[append_count] = item
                append_count = append_count+1
                skippy = False

        event_identifier = datum[2]

        # parsing API command
        if event_identifier == "###":
            action_specifier = datum[3]
            cmd1 = datum[4]
            key1 = datum[5]
            val1 = datum[6]
            cmd2 = datum[7]
            key2 = datum[8]
            val2 = datum[9]
            delim = datum[10]

            item = ""
            for i in range(0,10):
                point = datum[i]
                item += str(point) + ","
            item = item[:-1]

            apioutfile.write("%s\n" % (item))
            print("wrote api event #%d line #%d from log #%d" % (api_event_count, linenum, log_count))
            linenum = linenum+1
            total_log_lines = total_log_lines+1
            api_event_count += 1

        # parsing autonomous operation event
        elif event_identifier == "$$$":
            
            marker_id = -1
            marker_width = -1
            auton_state = ""
            item = ""

            if datum[3] == "SEARCHING":
                auton_state = datum[3]
                item += str(datum[0]) + ","
                item += str(datum[1]) + ","
                item += str(auton_state)
            if datum[5] == " FOLLOW_NAV": # yea, theres a space before...
                marker_id = datum[3]
                marker_width = datum[4]
                auton_state = datum[5]
                item += str(datum[0]) + ","
                item += str(datum[1]) + ","
                item += str(auton_state) + ","
                item += str(marker_id) + ","
                item += str(marker_width)
            elif datum[5] == " PERFORM_ACTION": # yea, theres a space before...
                marker_id = datum[3]
                marker_width = datum[4]
                auton_state = datum[5]
                item += str(datum[0]) + ","
                item += str(datum[1]) + ","
                item += str(auton_state) + ","
                item += str(marker_id) + ","
                item += str(marker_width)
                
            autonoutfile.write("%s\n" % (item))
            print("wrote autonomous event #%d line #%d from log #%d" % (auton_event_count, linenum, log_count))
            linenum = linenum+1
            total_log_lines = total_log_lines+1
            auton_event_count += 1

        # parsing regular log line
        else:
            time = datum[0]
            motor_a_speed = datum[1]
            motor_a_dir = datum[2]
            motor_b_speed = datum[3]
            motor_b_dir = datum[4]
            motor_current = datum[5]
            servo_pos_arm_l = datum[6]
            servo_pos_arm_r = datum[7]
            servo_pos_end = datum[8]
            servo_pos_hopper = datum[9]
            servo_pos_lid = datum[10]
            servo_pos_extra = datum[11]
            servo_current = datum[12]
            led_front_l = datum[13]
            led_front_r = datum[14]
            led_back_l = datum[15]
            led_back_r = datum[16]
            imu_pitch = datum[17]
            imu_roll = datum[18]
            imu_yaw = datum[19]
            compass_heading = datum[20]
            gps_sats = datum[21]
            gps_hdop = datum[22]
            gps_latitude = datum[23]
            gps_longitude = datum[24]
            gps_altitude = datum[25]
            battery = datum[26]
            comm_xbee_latency = datum[27]
            comm_arduino_latency = datum[28]
            humidity = datum[29]
            temperature = datum[30]
            uv = datum[31]
            wind = datum[32]
            
            if append_count >= urad_ind_start+6: # checking to see if the uradmonitor data was logged properly

                uradmonitor_data_time = str(datum[urad_ind_start])
                uradmonitor_pm25_raw = str(datum[urad_ind_start+1])
                uradmonitor_pm10_raw = str(datum[urad_ind_start+2])
                uradmonitor_o2_raw = str(datum[urad_ind_start+3])
                uradmonitor_no2_raw = str(datum[urad_ind_start+4])
                uradmonitor_so2_raw = str(datum[urad_ind_start+5])
                uradmonitor_nh3_raw = str(datum[urad_ind_start+6])

                tempstr = uradmonitor_data_time.split(":")
                uradmonitor_time = tempstr[len(tempstr)-1]
                datum[urad_ind_start] = uradmonitor_time

                tempstr = uradmonitor_pm25_raw.split(":")
                uradmonitor_pm25 = tempstr[1]
                datum[urad_ind_start+1] = uradmonitor_pm25

                tempstr = str(uradmonitor_pm10_raw).split(":")
                uradmonitor_pm10 = tempstr[1]
                datum[urad_ind_start+2] = uradmonitor_pm10

                tempstr = str(uradmonitor_o2_raw).split(":")
                uradmonitor_o2 = tempstr[1]
                o2_val = float(uradmonitor_o2)
                o2_val += 10.0 # calibration adjustment
                uradmonitor_o2 = str(o2_val)
                datum[urad_ind_start+3] = uradmonitor_o2

                tempstr = str(uradmonitor_no2_raw).split(":")
                uradmonitor_no2 = tempstr[1]
                datum[urad_ind_start+4] = uradmonitor_no2

                tempstr = str(uradmonitor_so2_raw).split(":")
                uradmonitor_so2 = tempstr[1]
                datum[urad_ind_start+5] = uradmonitor_so2

                if uradmonitor_nh3_raw != '0':
                    tempstr = str(uradmonitor_nh3_raw).split(":")
                    if len(tempstr) >= 2:
                        uradmonitor_nh3 = tempstr[1]
                    if "\n" in uradmonitor_nh3:
                        uradmonitor_nh3 = uradmonitor_nh3[:-2]
                    datum[urad_ind_start+6] = uradmonitor_nh3
                else:
                    # this is actually an indicator that the whole line is borked
                    for i in range(urad_ind_start, urad_ind_start+6+1):
                        datum[i] = "N/A"

            else:
                for i in range(urad_ind_start, urad_ind_start+6+1):
                    datum[i] = "N/A"

            item = ""
            include_item = False
            point_index = 0
            for point in datum:
                include_item = checkToIncludeThisItem(point_index)
                if include_item == True:
                    item += str(point) + ","
                point_index = point_index+1
            item = item[:-1]

            if skippy == False:
                outfile.write("%s\n" % (item))
                print("wrote line #%d from log #%d" % (linenum, log_count))

                linenum = linenum+1
                total_log_lines = total_log_lines+1

outfile.close()
apioutfile.close()
autonoutfile.close()
print("-----------------")
print("job complete. wrote %d total lines (%d were api events, %d were auton events), with %d unicode errors" % (total_log_lines, api_event_count, auton_event_count, num_unicode_errors));






