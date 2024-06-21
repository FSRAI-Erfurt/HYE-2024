# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from motor_controller import MotorController
from joystick_controller import joystick_lesen
from normierung import Normierer
import sensor_controller

# Pinzuweisung
Joystick_X = 11
Joystick_Y = 7
Joystick_Taster = 13
EnableA = 12
MotorSteuerSignalA1 = 16
MotorSteuerSignalA2 = 18
EnableB = 40
MotorSteuerSignalB1 = 36
MotorSteuerSignalB2 = 38
LinienerkennungLinks = 29  
LinienerkennungRechts = 33

try:
    # GPIO-physische Nummerierung
    GPIO.setmode(GPIO.BOARD)

    # GPIO setup
    GPIO.setup(Joystick_X, GPIO.IN)
    GPIO.setup(Joystick_Y, GPIO.IN)
    GPIO.setup(Joystick_Taster, GPIO.IN)

    GPIO.setup(LinienerkennungLinks, GPIO.IN)
    GPIO.setup(LinienerkennungRechts, GPIO.IN)

    # Motoren initialisieren
    controller = MotorController(EnableA, MotorSteuerSignalA1, MotorSteuerSignalA2, EnableB, MotorSteuerSignalB1, MotorSteuerSignalB2)

    # Initialisierung der Normierer für wert_x und wert_y
    normierer_x = Normierer()
    normierer_y = Normierer()

    # Initialphase zum Hochfahren der Sensoren
    start_time = time.time()

    ####### Manueller Betrieb mit Joystick
    while True:
        x_Wert, y_Wert, schalter = joystick_lesen(Joystick_X, Joystick_Y, Joystick_Taster)
        
        # Wartezeit
        if time.time() - start_time < 3:
            print(f"Initial Phase - x-Wert: {x_Wert}, y-Wert: {y_Wert}")
            time.sleep(0.005)
            continue

        # Normierung der Werte
        x_normiert = normierer_x.normiere_wert(x_Wert)
        y_normiert = normierer_y.normiere_wert(y_Wert)

        # Ausgabe der normierten Werte
        print("x-Wert:", x_normiert , "y-Wert:", y_normiert )

        # Geschwindigkeit und Richtung einstellen basierend auf normierten Werten
        if x_normiert <= 100 and y_normiert <= 100 and x_normiert >=- 100 and y_normiert >= -100:
            if y_normiert >= 0:
                direction_a = "forward"
            else:
                direction_a = "backward"
            speed_a = abs(y_normiert)  # Geschwindigkeit in Prozent

            if x_normiert >= 0:
                direction_b = "forward"
            else:
                direction_b = "backward"
            speed_b = abs(x_normiert)  # Geschwindigkeit in Prozent

            controller.set_motor_a(speed=speed_a, direction=direction_a)
            controller.set_motor_b(speed=speed_b, direction=direction_b)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("Programm beendet")

finally:
    GPIO.cleanup()  # GPIOs aufräumen für alle Pins
    controller.cleanup()  # Motoren aufräumen
