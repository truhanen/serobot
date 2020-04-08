
import asyncio as aio

import RPi.GPIO as GPIO

from ._pin_numbers import (
    bcm_right_motor_pwm,
    bcm_left_motor_pwm,
    bcm_right_motor_1,
    bcm_right_motor_2,
    bcm_left_motor_1,
    bcm_left_motor_2
)


class Motors:
    # PWM parameters
    pwm_freq = 500
    dc_move = 50  # Duty cycle for moving forwards/backwards
    dc_turn = 30  # Duty cycle for turning

    def __init__(self):
        # Setup outputs
        output_channels = [
            bcm_left_motor_1,
            bcm_left_motor_2,
            bcm_right_motor_1,
            bcm_right_motor_2,
            bcm_left_motor_pwm,
            bcm_right_motor_pwm,
        ]
        GPIO.setup(output_channels, GPIO.OUT, initial=GPIO.LOW)

        # Setup PWMs
        self._right_motor_pwm = GPIO.PWM(
            bcm_right_motor_pwm, self.pwm_freq)
        self._left_motor_pwm = GPIO.PWM(
            bcm_left_motor_pwm, self.pwm_freq)

        self._right_motor_pwm.start(self.dc_move)
        self._left_motor_pwm.start(self.dc_move)

    def __del__(self):
        self.stop()

    def _set_dc(self, left, right):
        """
        Arguments
        =========
        left|right: int, [-100, 100]
            Duty cycle for the left|right motor. Negative value sets
            the motor to go backwards.
        """
        # Default values when left == 0, right == 0
        left_1_state = GPIO.LOW
        left_2_state = GPIO.LOW
        right_1_state = GPIO.LOW
        right_2_state = GPIO.LOW

        if left > 0 and left <= 100:
            left_1_state = GPIO.LOW
            left_2_state = GPIO.HIGH
        elif left < 0 and left >= -100:
            left_1_state = GPIO.HIGH
            left_2_state = GPIO.LOW

        if right > 0 and right <= 100:
            right_1_state = GPIO.LOW
            right_2_state = GPIO.HIGH
        elif right < 0 and right >= -100:
            right_1_state = GPIO.HIGH
            right_2_state = GPIO.LOW

        self._left_motor_pwm.ChangeDutyCycle(abs(left))
        self._right_motor_pwm.ChangeDutyCycle(abs(right))

        GPIO.output(*zip(
            (bcm_left_motor_1, left_1_state),
            (bcm_left_motor_2, left_2_state),
            (bcm_right_motor_1, right_1_state),
            (bcm_right_motor_2, right_2_state),
        ))

    def stop(self):
        self._set_dc(0, 0)

    def move_forward(self):
        self._set_dc(self.dc_move, self.dc_move)

    def move_backward(self):
        self._set_dc(-self.dc_move, -self.dc_move)

    def turn_left(self):
        self._set_dc(-self.dc_turn, self.dc_turn)

    def turn_right(self):
        self._set_dc(self.dc_turn, -self.dc_turn)

    async def async_move_forward(self, duration=.5):
        """
        Parameters
        ----------
        duration : Number
            Duration of the movement in seconds.
        """
        self.move_forward()
        await aio.sleep(duration)
        self.stop()

    async def async_move_backward(self, duration=.5):
        """
        Parameters
        ----------
        duration : Number
            Duration of the movement in seconds.
        """
        self.move_backward()
        await aio.sleep(duration)
        self.stop()

    async def async_turn_left(self, duration=.5):
        """
        Parameters
        ----------
        duration : Number
            Duration of the turn in seconds.
        """
        self.turn_left()
        await aio.sleep(duration)
        self.stop()

    async def async_turn_right(self, duration=.5):
        """
        Parameters
        ----------
        duration : Number
            Duration of the turn in seconds.
        """
        self.turn_right()
        await aio.sleep(duration)
        self.stop()
