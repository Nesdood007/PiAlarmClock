# This is an alarm clock program for a raspberry pi.
# Brady O'Leary - 15 Oct 2017

import datetime
import RPi.GPIO as GPIO
import fileinput
import time
#import time

#Alarm Time and Date
alarmDateTime = None
isArmed = False

# Pin that beeper is connected to
BEEP_PIN = 7
BTN_PIN = 11

# Enable the Alarm
def arm():
  global isArmed
  isArmed = True
  print("Armed")

def disarm():
  global isArmed
  isArmed = False
  
# Interpret user input commands
def command():
  exit = False
  for line in sys.stdin:
    if line == "exit" or line == "quit":
      break
  
# Set Alarm Time
def alarmTime(hour, min, sec):
  alarmTime = datetime.time(hour, min, sec)
  currTime = datetime.datetime.now().time()
  alarmDate = datetime.datetime.now().date()
  if (currTime > alarmTime):
    alarmDate += datetime.timedelta(1)
    print("Fixed")
  global alarmDateTime
  print(alarmDate, alarmTime)
  alarmDateTime = datetime.datetime.combine(alarmDate, alarmTime)
  
# Takes User Input before being given to command.
# Executed when program is started.
def initTime():
  inGood = False
  while (not inGood):
    print("Enter Alarm Time (24 Hour)...")
    print("Hour:")
    hour = int(input())
    print("Minute:")
    min = int(input())
    print("Second:")
    sec = int(input())
    if (hour >= 0 and hour < 24 and min >= 0 and min < 60 and sec >= 0 and sec < 60):
      inGood = True
    else:
      print("Invalid Input.")
  alarmTime(hour, min, sec)
  
# Checks to see if the alarm needs to go off
def checkTime():
  if (alarmDateTime < datetime.datetime.now()):
    soundAlarm()
    
# Initialize the Pi
def init():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(BEEP_PIN, GPIO.OUT)
  GPIO.setup(BTN_PIN, GPIO.IN, GPIO.PUD_UP)

# Clean up after the program is finished
def clean():
  GPIO.cleanup()
# Sets off alarm
def soundAlarm():
  GPIO.output(BEEP_PIN, GPIO.HIGH)
  # Pin value is 0 while down
  while (GPIO.input(BTN_PIN) == 1):
    pass
    #Wait for the button to be pushed before turning off alarm
  GPIO.output(BEEP_PIN, GPIO.LOW)
  disarm()
  
#Main Function. Will be called  
def main():
  init()
  initTime()
  arm()
  #print(isArmed)
  while(isArmed):
    time.sleep(30) #Check only every half minute, since we don't need to constantly check the time
    checkTime()
  clean()
    
# Define Other Constants and things here
main() #Starts the program