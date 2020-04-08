
import asyncio as aio

import RPi.GPIO as GPIO

from ._pin_numbers import (
    bcm_left_ir_proximity_sensor,
    bcm_right_ir_proximity_sensor
)


class ProximitySensors:
    def __init__(self):
        GPIO.setup(bcm_left_ir_proximity_sensor, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(bcm_right_ir_proximity_sensor, GPIO.IN, GPIO.PUD_UP)

    def get_left_proximity(self):
        """
        Returns
        -------
        triggered : bool
            True if the left sensor is triggered.
        """
        return GPIO.input(bcm_left_ir_proximity_sensor) == 0

    def get_right_proximity(self):
        """
        Returns
        -------
        triggered : bool
            True if the right sensor is triggered.
        """
        return GPIO.input(bcm_right_ir_proximity_sensor) == 0

    async def async_get_left_proximity(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_left_proximity)

    async def async_get_right_proximity(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_right_proximity)
