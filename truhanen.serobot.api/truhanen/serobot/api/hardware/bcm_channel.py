
from enum import IntEnum


class BcmChannel(IntEnum):
    """Pin numbers, BCM"""
    # Motors
    motor_left_1 = 12  # Backward
    motor_left_2 = 13  # Forward
    motor_right_1 = 20  # Backward
    motor_right_2 = 21  # Forward
    motor_left_pwm = 6
    motor_right_pwm = 26

    # Buzzer
    buzzer = 4

    # LED's
    leds = 18

    # Sensors

    # Ultrasonic distance sensor
    ultrasonic_emitter = 22
    ultrasonic_sensor = 27

    # IR proximity sensor
    proximity_sensor_left = 16
    proximity_sensor_right = 19

    # IR remote controller sensor
    remote_control_sensor = 17

    # IR line tracker sensors
    line_trackers_sensors = 23
    line_trackers_address = 24
    line_trackers_clock = 25
    line_trackers_conversation = 5
