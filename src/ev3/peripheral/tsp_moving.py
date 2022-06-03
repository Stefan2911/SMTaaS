#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sound import Sound

coordinates = {
    1: (1, 1), 2: (1, 2), 3: (1, 3),
    4: (2, 1), 5: (2, 2), 6: (2, 3),
    7: (3, 1), 8: (3, 2), 9: (3, 3),
}

motor = MoveTank(OUTPUT_B, OUTPUT_C)
sound = Sound()


def move(value):
    # move
    forward = 1
    if value < 0:
        forward = -1
    motor.on_for_seconds(left_speed=40 * forward, right_speed=40 * forward, seconds=abs(value))


def change_direction_to_right():
    motor.on_for_seconds(left_speed=-10, right_speed=-10, seconds=1.5)
    motor.on_for_seconds(left_speed=0, right_speed=10, seconds=3)
    motor.on_for_seconds(left_speed=-10, right_speed=0, seconds=0.35)


def change_direction_to_down():
    motor.on_for_seconds(left_speed=-10, right_speed=-10, seconds=1.5)
    motor.on_for_seconds(left_speed=10, right_speed=0, seconds=3)
    motor.on_for_seconds(left_speed=0, right_speed=-10, seconds=0.35)


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
        sound.speak("move to")
        sound.speak(str(stops[i + 1]))
        looking_direction = move_to(stops[i], stops[i + 1], looking_direction)
    if looking_direction == 'down':
        change_direction_to_right()


# an example
move_with_stops([1, 3, 9, 5, 1])
