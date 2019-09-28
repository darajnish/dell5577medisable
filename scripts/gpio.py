#!/usr/bin/python

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM);
print('Setting BCM pin 23 as INPUT pull UP...')
GPIO.setup(23, GPIO.IN, GPIO.PUD_UP);
print('Setting BCM pin 24 as INPUT pull UP...')
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP);
print('Current Value of BCM pin 23: '+ GPIO.input(23))
print('Current Value of BCM pin 24: '+ GPIO.input(24))
