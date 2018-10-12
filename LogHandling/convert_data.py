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

for log_count in range(0, NUM_LOGS): # go through each of the log files

    total_filename = DIR + "/LOG_" + str(log_count) + ".csv"
    f = open(total_filename, 'r')
    
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
            servo_pos_arm_end = datum[8]
            servo_pos_arm_hopper = datum[9]
            servo_pos_arm_lid = datum[10]
            servo_pos_arm_extra = datum[11]
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
            for point in datum:
                item += str(point) + ","
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








