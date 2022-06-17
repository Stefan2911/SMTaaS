#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sound import Sound

coordinates = {
    0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3),
    4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (1, 3),
    8: (2, 0), 9: (2, 1), 10: (2, 2), 11: (2, 3),
    12: (3, 0), 13: (3, 1), 14: (3, 2), 15: (3, 3)
}

coordinates_simple = {
    0: (0, 0), 1: (0, 1), 2: (0, 2),
    3: (1, 0), 4: (1, 1), 5: (1, 2),
    6: (2, 0), 7: (2, 1), 8: (2, 2),
}

motor = MoveTank(OUTPUT_B, OUTPUT_C)
sound = Sound()

TURN_SPEED = 10
MOVE_SPEED = 40


def move(value):
    forward = 1
    if value < 0:
        forward = -1
    motor.on_for_seconds(left_speed=MOVE_SPEED * forward, right_speed=MOVE_SPEED * forward, seconds=abs(value))


def change_direction_to_right():
    motor.on_for_seconds(left_speed=TURN_SPEED * -1, right_speed=TURN_SPEED * -1, seconds=1.5)
    motor.on_for_seconds(left_speed=0, right_speed=TURN_SPEED, seconds=3)
    motor.on_for_seconds(left_speed=TURN_SPEED * -1, right_speed=0, seconds=0.35)


def change_direction_to_down():
    motor.on_for_seconds(left_speed=TURN_SPEED * -1, right_speed=TURN_SPEED * -1, seconds=1.5)
    motor.on_for_seconds(left_speed=TURN_SPEED, right_speed=0, seconds=3)
    motor.on_for_seconds(left_speed=0, right_speed=TURN_SPEED * -1, seconds=0.35)


def move_to(starting_point, destination, view_direction):
    destination_coordinates = coordinates.get(destination)
    starting_point_coordinates = coordinates.get(starting_point)
    move_action = (destination_coordinates[0] - starting_point_coordinates[0],
                   destination_coordinates[1] - starting_point_coordinates[1])
    if move_action[0] != 0:
        if view_direction == 'right':
            change_direction_to_down()
        move(move_action[0])
        view_direction = 'down'
    if move_action[1] != 0:
        if view_direction == 'down':
            change_direction_to_right()
        move(move_action[1])
        view_direction = 'right'
    return view_direction


def move_with_stops(stops):
    view_direction = 'right'
    for i in range(len(stops) - 1):
        sound.speak("move to")
        sound.speak(str(stops[i + 1]))
        view_direction = move_to(stops[i], stops[i + 1], view_direction)
    if view_direction == 'down':
        change_direction_to_right()


if __name__ == "__main__":
    move_with_stops([0, 1, 2, 3, 7, 11, 15, 14, 13, 12, 8, 9, 10, 6, 5, 4, 0])
    # simple:
    move_with_stops([0, 1, 2, 5, 4, 7, 6, 3, 0])
