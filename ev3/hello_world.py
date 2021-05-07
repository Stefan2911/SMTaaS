#!/usr/bin/env python3

from ev3dev2.led import Leds
from ev3dev2.sound import Sound

leds = Leds()
leds.set_color("LEFT", "GREEN")
leds.set_color("RIGHT", "RED")

sound = Sound()
sound.speak('Hi!')
