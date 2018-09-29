#!/usr/bin/env python3

# Read the raw logs to find the "runs" - sequences of logs
# with no gapes of more than 120 seconds.
#
# usage: runs.py <<input dir>>
#
# Assumes the logs are named LOGn.csv, where n is a number
# and the first log is 0 and they are sequentially numbered.
#
# by Erin RobotGrrl for Robot Missions
# robotmissions.org
# June 7, 2018
# 2018-09-03 Adapted by bjb for this new use

import datetime
import logging
import sys
import os
import re

# XXX Assumed the times are 24-hour times ... example logs seem to bear that out
def time_in_seconds_since_midnight(t1):
    answer = t1.second
    answer += t1.minute * 60
    answer += t1.hour * 60 * 60
    return answer

# XXX should we worry about midnight-rollover?
def time_subtract(t1, t2):
    '''Theoretically, we should only be reading times in chronological order
so the times will be monotonically increasing'''
    t2s = time_in_seconds_since_midnight(t2)
    t1s = time_in_seconds_since_midnight(t1)
    return t1s - t2s

def extract_logfile_num(fname):
    '''Given a logfile name of type LOG_NN.csv, extract the NN and convert to integer'''
    fname = fname[4:]
    num_rex = re.compile(r'^.*/LOG_([0-9]+)\.[Cc][Ss][Vv]$')
    mo = num_rex.search(fname)
    answer = None
    if mo:
        answer = int(mo.group(1))
    else:
        answer = None
    print('extract_logfile_num:  {} {} {}'.format(fname, mo.group(1), answer))
    return answer

class RunDuration():
    def __init__(self, start, filename, stop=None):
        self.start = start
        self.stop = stop
        self.filename_start = filename
        self.filename_end = ''

    def __str__(self):
        return '{} {} {} {} {}'.format(
            self.start, self.stop,
            time_subtract(self.stop, self.start),
            self.filename_start, self.filename_end)

class RunDurations():
    def __init__(self):
        self.latest_time=datetime.time(hour=0, minute=0, second=0)
        self.runs = list()
        self.this_run_duration = None

    def account_for_time(self, time_string, filename):
        logger.debug('account for time:  {}  {}'.format(filename, time_string))
        hh, mm, ss = time_string.split(':')
        tt = datetime.time(hour=int(hh), minute=int(mm), second=int(ss))
        duration = time_subtract(tt, self.latest_time)
        if duration > 120:
            flag = '*'
        else:
            flag = ' '
        logger.debug('last time {}  now {} this duration is {} {}'.format(
            self.latest_time, tt, duration, flag))
        self.latest_time = tt
        if self.this_run_duration:
            logger.debug('another time for this Duration')
            if duration > 120:
                # close up the last run

                logger.debug('close up last run and start a new one')
                # start this new run
                self.this_run_duration.stop = self.latest_time
                self.this_run_duration.filename_end = filename
                self.runs.append(self.this_run_duration)
                self.this_run_duration = RunDuration(tt, filename)
        else:
            # first time in first run
            logger.debug('Make a new Duration obj')
            self.this_run_duration = RunDuration(tt, filename)

    def close(self, filename):
        if self.this_run_duration:
            self.this_run_duration.filename_end = filename
            self.this_run_duration.stop = self.latest_time
            self.runs.append(self.this_run_duration)

    def __str__(self):
        answer = ''
        answer = '\n'.join([str(x) for x in self.runs])
        return answer
    

loglevel = logging.ERROR
logger = logging.getLogger('duration')
logger.setLevel(loglevel)
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(loglevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


if len(sys.argv) >= 1:
    DIR = sys.argv[1]
else:
    print("Please specify a directory")
    exit()

list_dir = os.listdir(DIR)

NUM_LOGS = 0
logfiles = list()
for root, dirs, files in os.walk(DIR):
    for filename in files:
        if filename.startswith("LOG"):
            NUM_LOGS += 1
            print('Adding name {} to list'.format(filename))
            logfiles.append(os.path.join(root, filename))

logfiles = sorted(logfiles, key=extract_logfile_num)

total_log_lines = 0
num_unicode_errors = 0

rd = RunDurations()

for total_filename in logfiles:

    print('handling filename {}'.format(total_filename))
    
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
    print("{}  Number of lines = {}".format(total_filename, number_of_lines))
    f.close()

    f = open(total_filename, 'r', encoding="utf-8")
    try:
        s1 = f.readline() # skip the first one, already read it previously
    except UnicodeDecodeError:
        print("!!! A UnicodeDecodeError has occured on this line:");
        print(s)
        print("We will skip it")
        num_unicode_errors += 1

    #for line in f: # go through each of the lines
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

        item = splittystring[0]

        if item != ' ' and item != '' and item != '\n':
            rd.account_for_time(item, total_filename)

rd.close(total_filename)
print("-----------------");

print('run durations')
print('{}'.format(rd))
print('number of unicode errors {}'.format(num_unicode_errors))
