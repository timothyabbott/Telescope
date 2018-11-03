#!/usr/bin/env python3



import pigpio

import MStepper

import time

class MicroStepControl:

  def __init__(self):

    pi = pigpio.pi()



    #create a  16 micro-step stepper

    m1 = MStepper.MStepper(pi,1)

    #define your own GPIO pin
    m1.CoilA = 14
    m1.CoilB = 15
    m1.CoilC = 18
    m1.CoilD = 23
    m1.PwmAC = 20
    m1.PwmBD = 21

    #set GPIO and calculate GPIO Table

    m1.setGPIO()

    #Activate coil and set position
    m1.setStepper(0)
    print ("coil activated")



    m1.delay = 0.45

# move a whole step

  def track():
    m1.move(16)

  def stop():
    m1.stop()



