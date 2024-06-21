# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

def entladen(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.0005)

def ladezeit(pin):
    GPIO.setup(pin, GPIO.IN)
    count = 0
    while not GPIO.input(pin):
        count += 1
    return count

def joystick_lesen(joystick_x, joystick_y, joystick_taster):
    entladen(joystick_x)
    wert_x = ladezeit(joystick_x)
    
    entladen(joystick_y)
    wert_y = ladezeit(joystick_y)

    schalter_zustand = GPIO.input(joystick_taster)
    # print("x-Wert:", wert_x, "y-Wert:", wert_y)
    return wert_x, wert_y, schalter_zustand
