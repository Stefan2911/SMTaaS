#!/usr/bin/env python3
from time import sleep

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound


def move():
    motor = MoveTank(OUTPUT_B, OUTPUT_C)
    ultrasonic_sensor = UltrasonicSensor()
    sound = Sound()
    try:
        while True:
            # Start robot moving forward
            motor.on(left_speed=100, right_speed=100)

            # Wait until robot less than 3cm from obstacle
            while ultrasonic_sensor.distance_centimeters > 20:
                sleep(0.01)

            sound.beep()
            motor.off()
            motor.on_for_seconds(left_speed=0, right_speed=-10, seconds=4)

    finally:
        motor.off()


move()
