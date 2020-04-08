
import RPi.GPIO as GPIO


# General settings whenever the values in this module are used
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Pin numbers, BCM

# Motors
bcm_left_motor_1 = 12  # Backward
bcm_left_motor_2 = 13  # Forward
bcm_right_motor_1 = 20  # Backward
bcm_right_motor_2 = 21  # Forward
bcm_left_motor_pwm = 6
bcm_right_motor_pwm = 26

# Buzzer
bcm_buzz = 4

# LEDs
bcm_led = 18

# Sensors
# Ultrasonic distance sensor
bcm_ultrasonic_emitter = 22
bcm_ultrasonic_sensor = 27

# IR proximity sensor
bcm_left_ir_proximity_sensor = 16
bcm_right_ir_proximity_sensor = 19

# IR remote controller sensor
bcm_ir_remote_sensor = 17

# IR line tracker sensors
bcm_ir_tracker_sensors = 23
bcm_ir_tracker_address = 24
bcm_ir_tracker_clock = 25
bcm_ir_tracker_cs = 5
