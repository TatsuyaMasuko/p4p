#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

LedPin = 15    # pin15

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
    GPIO.output(LedPin, GPIO.HIGH) # Set pin to high(+3.3V) to off the led

def loop():
    while True:
        for i in range(1,6):
            print ('...led on')
            GPIO.output(LedPin, GPIO.LOW)  # led on
            time.sleep(0.1)
            print ('led off...')
            GPIO.output(LedPin, GPIO.HIGH) # led off
            time.sleep(0.1)
        input("押す CR")

def destroy():
    GPIO.output(LedPin, GPIO.HIGH)     # led off
    GPIO.cleanup()                     # Release resource
    print('\n- cleanup GPIO -')

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

