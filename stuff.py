#!/usr/bin/pythonRoot
# bring in the libraries
import logging
import time
import datetime
import RPi.GPIO as G
from flup.server.fcgi import WSGIServer
import sys, urlparse
import time
trackSpeed = 1.8
delay = 0.1
import pigpio
import MStepper
pi = pigpio.pi()
#there are 130 revolutions of the slow motion control for a complete revolution
#of the telescope.
# there are 200 steps for a complete revolution of the motor.
#200 * 130 = 26000
#86400 ( seconds in a day) / 2600 = 3.32307692308 seconds per movement
#1.8 seconds when half stepping.


run = "go"
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info(datetime.datetime.now())
# set up our GPIO pins
G.setmode(G.BCM)
G.setup(18, G.OUT)
enable_a = 20
enable_b = 21


# Enable pins for IN1-4 to control step sequence
coil_A_1_pin = 14
coil_A_2_pin = 15
coil_B_1_pin = 18
coil_B_2_pin = 23

# Set pin states
G.setup(enable_a, G.OUT)
G.setup(enable_b, G.OUT)
G.setup(coil_A_1_pin, G.OUT)
G.setup(coil_A_2_pin, G.OUT)
G.setup(coil_B_1_pin, G.OUT)
G.setup(coil_B_2_pin, G.OUT)

# Set ENA and ENB to high to enable stepper
G.output(enable_a, True)
G.output(enable_b, True)

# create microstepper
microSteps = 16
m1 = MStepper.MStepper(pi,microSteps)
m1.setGPIO()

# Function for step sequence
def setStep(w1, w2, w3, w4):
  G.output(coil_A_1_pin, w1)
  G.output(coil_A_2_pin, w2)
  G.output(coil_B_1_pin, w3)
  G.output(coil_B_2_pin, w4)

def forwards():
  while run != "stop":
    setStep(0,0,1,0)
    time.sleep(delay)
    setStep(0,1,0,0)
    time.sleep(delay)
    setStep(0,0,0,1)
    time.sleep(delay)
    setStep(1,0,0,0)
    time.sleep(delay)
  setStep(0,0,0,0)

def backwards():
  while run != "stop":
    setStep(1,0,0,1)
    time.sleep(delay)
    setStep(0,1,0,1)
    time.sleep(delay)
    setStep(0,1,1,0)
    time.sleep(delay)
    setStep(1,0,1,0)
    time.sleep(delay)
  setStep(0,0,0,0)

def track():
  startTime = datetime.datetime.now()
  logging.info("complete turn started at...")
  logging.info(startTime)
  #while run != "stop":
  for i in range(0,100):
    logging.info(datetime.datetime.now()-startTime)
    m1.move(1600)
  logging.info("complete turn took...")
  logging.info(datetime.datetime.now()-startTime)

  m1.stop()
  

def app(environ, start_response):

  # start our http response 
  start_response("200 OK", [("Content-Type", "text/html")])
  # look for inputs on the URL
  i = urlparse.parse_qs(environ["QUERY_STRING"])
  yield ('&nbsp;') # flup expects a string to be returned from this function
  # if there's a url variable named 'q'
  global run

  if "q" in i:
    if i["q"][0] == "L":
      run = True
      forwards()
    if i["q"][0] == "R":
      run = True
      backwards()
    if i["q"][0] == "S":
      run = "stop"
    if i["q"][0] == "T":
      run = True
      track()

   # if i["q"][0]=="X":
   #   run = "stop":
#by default, Flup works out how to bind to the web server for us, so just call i$
WSGIServer(app).run()

