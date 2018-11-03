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
    count = 0
    setStep(1,0,1,0)
    print(1)
    time.sleep(trackSpeed)
    setStep(0,0,1,0)
    print(2)
    time.sleep(trackSpeed)
    setStep(0,1,1,0)
    print(3)
    time.sleep(trackSpeed)
    setStep(0,1,0,0)
    print(4)
    time.sleep(trackSpeed)
    setStep(0,1,0,1)
    print(5)
    time.sleep(trackSpeed)
    setStep(0,0,0,1)
    print(6)
    time.sleep(trackSpeed)
    setStep(1,0,0,1)
    print(7)
    time.sleep(trackSpeed)
    setStep(1,0,0,0)
    print(8)
    time.sleep(trackSpeed)

track()
G.cleanup()
