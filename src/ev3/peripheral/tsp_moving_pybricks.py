#!/usr/bin/env micropython

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

coordinates = {
    1: (1, 1), 2: (1, 2), 3: (1, 3),
    4: (2, 1), 5: (2, 2), 6: (2, 3),
    7: (3, 1), 8: (3, 2), 9: (3, 3),
}


def move(value):
    # move
    forward = 1
    if value < 0:
        forward = -1
    robot.straight(value * 10 * forward)


def change_direction_to_right():
    robot.turn(-90)


def change_direction_to_down():
    robot.turn(90)


def move_to(starting_point, destination, looking_direction):
    destination_coordinates = coordinates.get(destination)
    starting_point_coordinates = coordinates.get(starting_point)
    move_action = (destination_coordinates[0] - starting_point_coordinates[0],
                   destination_coordinates[1] - starting_point_coordinates[1])
    if move_action[0] != 0:
        if looking_direction == 'right':
            change_direction_to_down()
        move(move_action[0])
        looking_direction = 'down'
    if move_action[1] != 0:
        if looking_direction == 'down':
            change_direction_to_right()
        move(move_action[1])
        looking_direction = 'right'
    return looking_direction


def move_with_stops(stops):
    looking_direction = 'right'
    for i in range(len(stops) - 1):
        looking_direction = move_to(stops[i], stops[i + 1], looking_direction)
        ev3.speaker.say("move to: " + stops(i))
    if looking_direction == 'down':
        change_direction_to_right()


# an example
move_with_stops([1, 3, 9, 5, 1])
