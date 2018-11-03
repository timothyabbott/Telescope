#!/usr/bin/pythonRoot
# bring in the libraries
import RPi.GPIO as G
from flup.server.fcgi import WSGIServer
import sys, urlparse
import time
trackSpeed = 1.8
#there are 120 revolutions of the slow motion control for a complete revolution
#of the telescope.
# there are 200 steps for a complete revolution of the motor.
#200 * 120 = 24000
#864000 ( seconds in a day) / 2400 = 3.6 seconds per movement
#1.8 seconds when half stepping.


delay = 0.05
steps =200/4
run = "go"

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
    # Function for step sequence
def setStep(w1, w2, w3, w4):
  G.output(coil_A_1_pin, w1)
  G.output(coil_A_2_pin, w2)
  G.output(coil_B_1_pin, w3)
  G.output(coil_B_2_pin, w4)

def forwards():
  while run != "stop":
    setStep(0,1,1,0)
    time.sleep(delay)
    setStep(0,1,0,1)
    time.sleep(delay)
    setStep(1,0,0,1)
    time.sleep(delay)
    setStep(1,0,1,0)
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
  while run != "stop":
    setStep(1,0,1,0)
    time.sleep(trackSpeed)
    setStep(0,0,1,0)
    time.sleep(trackSpeed)
    setStep(0,1,1,0)
    time.sleep(trackSpeed)
    setStep(0,1,0,0)
    time.sleep(trackSpeed)
    setStep(0,1,0,1)
    time.sleep(trackSpeed)
    setStep(0,0,0,1)
    time.sleep(trackSpeed)
    setStep(1,0,0,1)
    time.sleep(trackSpeed)
    setStep(1,0,0,0)
    time.sleep(trackSpeed)
# all of our code now lives within the app() function which is called for each h$
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

