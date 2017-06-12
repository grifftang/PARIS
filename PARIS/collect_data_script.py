# -----------------------------------------------------------------------
#
# (c) Copyright 1997-2013, SensoMotoric Instruments GmbH
# 
# Permission  is  hereby granted,  free  of  charge,  to any  person  or
# organization  obtaining  a  copy  of  the  software  and  accompanying
# documentation  covered  by  this  license  (the  "Software")  to  use,
# reproduce,  display, distribute, execute,  and transmit  the Software,
# and  to  prepare derivative  works  of  the  Software, and  to  permit
# third-parties to whom the Software  is furnished to do so, all subject
# to the following:
# 
# The  copyright notices  in  the Software  and  this entire  statement,
# including the above license  grant, this restriction and the following
# disclaimer, must be  included in all copies of  the Software, in whole
# or  in part, and  all derivative  works of  the Software,  unless such
# copies   or   derivative   works   are   solely   in   the   form   of
# machine-executable  object   code  generated  by   a  source  language
# processor.
# 
# THE  SOFTWARE IS  PROVIDED  "AS  IS", WITHOUT  WARRANTY  OF ANY  KIND,
# EXPRESS OR  IMPLIED, INCLUDING  BUT NOT LIMITED  TO THE  WARRANTIES OF
# MERCHANTABILITY,   FITNESS  FOR  A   PARTICULAR  PURPOSE,   TITLE  AND
# NON-INFRINGEMENT. IN  NO EVENT SHALL  THE COPYRIGHT HOLDERS  OR ANYONE
# DISTRIBUTING  THE  SOFTWARE  BE   LIABLE  FOR  ANY  DAMAGES  OR  OTHER
# LIABILITY, WHETHER  IN CONTRACT, TORT OR OTHERWISE,  ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE  SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# -----------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from iViewXAPI import  *            #iViewX library
from iViewXAPIReturnCodes import *
import threading
import time

# ---------------------------------------------
#---- connect to iViewX
# ---------------------------------------------

# Ask user for participant number/id
participant_id = raw_input('Enter participant ID: ')
today = `datetime.now().month` + "_" + `datetime.now().day` + "_" + `datetime.now().year`
time_now = `datetime.now().hour` + "_" + `datetime.now().minute`
file_name = participant_id + "_" + today + "_" + time_now + '.csv'
data = open(file_name,'wb')
print "Data will save to the file: " + file_name
writer = csv.writer(data, delimiter = ',')
writer.writerow(["Participant ID: " + participant_id, "Date: " + today, "Time: " + time_now]) #check this line again
heading = ["ComputerClock_Timestamp", "Avg_GazeX", "Avg_GazeY", "LeftEye_GazeX", "LeftEye_GazeY", "RightEye_GazeX", "RightEye_GazeY"]

print "Preparing eye-tracker..."

res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p("iViewXSDK_Python_SimpleExperiment.txt"))
res = iViewXAPI.iV_Connect(c_char_p('127.0.0.1'), c_int(4444), c_char_p('127.0.0.1'), c_int(5555))
if res != 1:
    HandleError(res)
    exit(0)

res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
# print "iV_GetSystemInfo: " + str(res)
# print "Samplerate: " + str(systemData.samplerate)
# print "iViewX Version: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber)
# print "iViewX API Version: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber)


# ---------------------------------------------
#---- configure and start calibration
# ---------------------------------------------

##num_points = int(raw_input("Set your number of points for Calibration (1, 2, 5, 9, or 13): "))
##
##calibrationData = CCalibration(num_points, 1, 0, 0, 1, 250, 220, 2, 30, b"")
##res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
### print "iV_SetupCalibration " + str(res)
##
##command = 0
##while (command != 'done'):
##    command = raw_input("Press Enter to begin eye-tracker Calibration.")
##    res = iViewXAPI.iV_Calibrate()
### print "iV_Calibrate " + str(res)
##
##    command = raw_input("Press Enter to begin eye-tracker Validation.")
##    res = iViewXAPI.iV_Validate()
### print "iV_Validate " + str(res)
##
##    res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 1)
##    print "iV_GetAccuracy " + str(res)
##    print "deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY)
##    print "deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRY)
##
##    command = raw_input("To finish Calibration and Validation, type 'done' and press Enter. Otherwise type 'retry' and press Enter.")
##    print command
##    
# TODO: implement loop to allow user to recalibrate (and revalidate) as needed.

# ---------------------------------------------
#---- define the callback functions
# ---------------------------------------------

def SampleCallback(sample):
    sample_data = []
    sample_data.append(`time.time()*1000`)
    sample_data.append(`(sample.leftEye.gazeX + sample.rightEye.gazeX)/2`)
    sample_data.append(`(sample.leftEye.gazeY + sample.rightEye.gazeY)/2`)
    sample_data.append(`sample.leftEye.gazeX`)
    sample_data.append(`sample.leftEye.gazeY`)
    sample_data.append(`sample.rightEye.gazeX`)
    sample_data.append(`sample.rightEye.gazeY`)
    writer.writerow(sample_data)
    return 0

def EventCallback(event):
    return 0


CMPFUNC = WINFUNCTYPE(c_int, CSample)
smp_func = CMPFUNC(SampleCallback)
sampleCB = False

CMPFUNC = WINFUNCTYPE(c_int, CEvent)
event_func = CMPFUNC(EventCallback)
eventCB = False


# ---------------------------------------------
#---- start DataStreaming
# ---------------------------------------------
    
class StoppableThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.run = True
        while self.run:
            res = iViewXAPI.iV_SetSampleCallback(smp_func)
            sampleCB = True
            res = iViewXAPI.iV_SetEventCallback(event_func)
            eventCB = True
            # time.sleep(0.0166) TODO: check whether we need to do this

    def stop(self):
        self.run = False

command = 0
while (command != 'start'):
    command = raw_input("Type 'start' and press Enter to begin eye-tracking: ")

print "Initiating eye-tracking."
# start recording in a background thread
thr = StoppableThread()
thr.start()

# wait for user to terminate recording
command = 0
while (command != 'quit'):
    command = raw_input("Type 'quit' and press Enter to terminate eye-tracking recording: ")

print "Terminating eye-tracking collection..."
# tell background thread to stop and wait for it to terminate
thr.stop()
thr.join()

# ---------------------------------------------
#---- stop recording and disconnect from iViewX
# ---------------------------------------------

print "Disconnecting from eye-tracker..."

res = iViewXAPI.iV_Disconnect()

print "Saving eye-tracking data..."

data.flush()
data.close()

print "Done!"
