
import asyncio as aio

from .bcm_channel import BcmChannel
from .gpio import GpioOutput, GpioPwm, GpioState


class Motors:
    # PWM parameters
    pwm_freq = 500
    dc_move = 50  # Duty cycle for moving forwards/backwards
    dc_turn = 30  # Duty cycle for turning

    def __init__(self):
        # Setup outputs.
        self._output_left_1 = GpioOutput(BcmChannel.motor_left_1, initial=GpioState.LOW)
        self._output_left_2 = GpioOutput(BcmChannel.motor_left_2, initial=GpioState.LOW)
        self._output_right_1 = GpioOutput(BcmChannel.motor_right_1, initial=GpioState.LOW)
        self._output_right_2 = GpioOutput(BcmChannel.motor_right_2, initial=GpioState.LOW)

        # Setup PWMs
        self._pwm_left = GpioPwm(
            BcmChannel.motor_left_pwm, frequency=self.pwm_freq,
            duty_cycle=self.dc_move)
        self._pwm_right = GpioPwm(
            BcmChannel.motor_right_pwm, frequency=self.pwm_freq,
            duty_cycle=self.dc_move)

        self._pwm_left.start()
        self._pwm_right.start()

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
        left_1_state = GpioState.LOW
        left_2_state = GpioState.LOW
        right_1_state = GpioState.LOW
        right_2_state = GpioState.LOW

        if left > 0 and left <= 100:
            left_1_state = GpioState.LOW
            left_2_state = GpioState.HIGH
        elif left < 0 and left >= -100:
            left_1_state = GpioState.HIGH
            left_2_state = GpioState.LOW

        if right > 0 and right <= 100:
            right_1_state = GpioState.LOW
            right_2_state = GpioState.HIGH
        elif right < 0 and right >= -100:
            right_1_state = GpioState.HIGH
            right_2_state = GpioState.LOW

        self._pwm_left.duty_cycle = abs(left)
        self._pwm_right.duty_cycle = abs(right)

        GpioOutput.set_multiple(*zip(
            (self._output_left_1, left_1_state),
            (self._output_left_2, left_2_state),
            (self._output_right_1, right_1_state),
            (self._output_right_2, right_2_state),
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
