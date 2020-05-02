
import asyncio as aio

from .bcm_channel import BcmChannel
from .gpio import GpioInput, GpioPull, GpioState


class ProximitySensors:
    def __init__(self):
        self._left_sensor = GpioInput(BcmChannel.proximity_sensor_left, pull=GpioPull.UP)
        self._right_sensor = GpioInput(BcmChannel.proximity_sensor_right, pull=GpioPull.UP)

    def get_left_proximity(self):
        """
        Returns
        -------
        triggered : bool
            True if the left sensor is triggered.
        """
        return self._left_sensor.state == GpioState.LOW

    def get_right_proximity(self):
        """
        Returns
        -------
        triggered : bool
            True if the right sensor is triggered.
        """
        return self._right_sensor.state == GpioState.LOW

    async def async_get_left_proximity(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_left_proximity)

    async def async_get_right_proximity(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_right_proximity)
