import signal
import u3
import csv
import time

SAMPLE_INTERVAL   = 30 #seconds
test_loops = 0

PIN_INPUTV = 0
PIN_OUTPUTV = 1

print("Start Logging")
d = u3.U3()
d.getCalibrationData()
#d.setFIOState(0, 0)
#d.setFIOState(1, 0)

logfile = open("testlog.csv", "wb")
logwriter = csv.writer(logfile, quoting=csv.QUOTE_NONNUMERIC)

logwriter.writerow(['Datetime', 'Elapsed Seconds', 'Input Voltage', 'Output Voltage'])

def sample_and_log():
   # prepare yourself
   global test_loops
   test_time = test_loops * SAMPLE_INTERVAL
   test_loops = test_loops + 1

   inv  = d.getAIN(u3.AIN(PositiveChannel=PIN_INPUTV, NegativeChannel=32))
   outv = d.getAIN(u3.AIN(PositiveChannel=PIN_OUTPUTV, NegativeChannel=32))

   logwriter.writerow([time.ctime(), test_time, inv, outv])

   logfile.flush()

sample_and_log()

signal.signal(signal.SIGALRM, sample_and_log)
signal.setitimer(signal.ITIMER_REAL, SAMPLE_INTERVAL, SAMPLE_INTERVAL)
while True:
    signal.pause()

logfile.close()

