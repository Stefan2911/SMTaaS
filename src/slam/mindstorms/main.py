#!/usr/bin/env python3
import logging
import socket

from ev3dev2.motor import (OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveSteering)
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound

logging.basicConfig()
logger = logging.getLogger('mindstorms')
logger.setLevel(level=logging.DEBUG)

DISTANCE_FACTOR = 36
ANGLE_FACTOR = 5.65
SCAN_POSITION_FACTOR = 3

MAX_VALID_MEASUREMENT = 100

PORT = 50000
SOUND_ON = False
sound = Sound()

receive_buffer = b""
end_char = b"\0"


def say(msg):
    if SOUND_ON:
        sound.speak(msg)
    logger.debug(msg)


# Init motors
steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)
motor_sensor = MediumMotor(OUTPUT_D)

# Init sensor
ultrasonic_sensor = UltrasonicSensor()
sensor_orientation = 0


def establish_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((socket.gethostname(), PORT))
    except OSError:
        say("Could not open a socket")
        exit(1)
    logger.debug("Hostname: " + socket.gethostname() + ", port:" + str(PORT))
    server_socket.listen(1)

    say('Ready to connect!')

    (cs, a) = server_socket.accept()
    return cs, a


logger.debug("Establishing connection")
client_socket, address = establish_connection()
logger.debug("Connection established")


def send_to_socket(socket, message):
    total = 0
    msg = message.encode() + end_char
    while total < len(msg):
        sent = socket.send(msg[total:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total += sent


def receive_from_socket(socket):
    global receive_buffer
    while end_char not in receive_buffer:
        chunk = socket.recv(1024)
        if chunk == b"":
            raise RuntimeError("Socket connection broken")
        receive_buffer += chunk
    end_char_loc = receive_buffer.index(end_char)
    msg = receive_buffer[:end_char_loc]
    receive_buffer = receive_buffer[end_char_loc + 1:]
    return msg.decode()


def move_forward(distance):
    logger.debug("Move forward for " + str(distance))
    steer_pair.on_for_degrees(steering=0, speed=30,
                              degrees=DISTANCE_FACTOR * distance)


def rotate(angle):
    logger.debug("Rotate for " + str(angle))
    steer_pair.on_for_degrees(steering=-100, speed=30,
                              degrees=ANGLE_FACTOR * angle)


def rotate_sensor(angle, block=True, speed=5):
    angle_scaled = angle * SCAN_POSITION_FACTOR
    motor_sensor.on_for_degrees(speed=speed,
                                degrees=angle_scaled,
                                block=block)
    global sensor_orientation
    sensor_orientation += angle_scaled


def rotate_sensor_to_zero_position():
    rotate_sensor(-sensor_orientation / SCAN_POSITION_FACTOR, speed=20)


def measure_and_send(angle):
    distance_centimeters = ultrasonic_sensor.distance_centimeters
    if distance_centimeters <= MAX_VALID_MEASUREMENT:
        msg = str(angle) + " " + str(distance_centimeters)
        logger.info("Measured " + str(distance_centimeters) + " at " + str(angle))
    else:
        msg = str(angle) + " " + str(distance_centimeters) + " FREE"
        logger.info("Looking at infinity " + str(angle))

    send_to_socket(client_socket, msg)


def scan(precision, num_scans, increasing):
    total_rotation = (num_scans - 1) * precision
    if not increasing:
        total_rotation = -total_rotation

    start_motor_position = motor_sensor.position
    next_scan_at = 0

    rotate_sensor(total_rotation, block=False)

    while motor_sensor.is_running:
        relative_motor_position = motor_sensor.position - start_motor_position
        if abs(relative_motor_position / SCAN_POSITION_FACTOR) >= next_scan_at:
            measure_and_send(next_scan_at)
            next_scan_at += precision

    # Check if the last measurement was made
    if next_scan_at <= total_rotation:
        measure_and_send(next_scan_at)

    send_to_socket(client_socket, "END")


with client_socket:
    try:
        while True:
            c = receive_from_socket(client_socket)
            if not c:
                break
            command, *params = c.split(" ")
            if command == "MOVE":
                move_forward(float(params[0]))
            elif command == "ROTATE":
                rotate(float(params[0]))
            elif command == "SCAN":
                precision = float(params[0])
                num_scans = float(params[1])
                increasing = params[2] == "True"
                scan(precision, num_scans, increasing)
            elif command == "ROTATESENSOR":
                rotate_sensor(float(params[0]), speed=20)
            else:
                logger.debug("Unknown command: " + command)
    except (KeyboardInterrupt, RuntimeError, OSError):
        pass
    except Exception as e:
        logger.error(e)

say("Shut down")
rotate_sensor_to_zero_position()
steer_pair.off()
motor_sensor.off()
