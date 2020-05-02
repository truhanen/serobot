
import time
import asyncio as aio

from .bcm_channel import BcmChannel
from .gpio import GpioOutput, GpioInput, GpioState


class DistanceSensor:
    def __init__(self):
        self._emitter = GpioOutput(BcmChannel.ultrasonic_emitter, initial=GpioState.LOW)
        self._sensor = GpioInput(BcmChannel.ultrasonic_sensor)

    def get_distance(self):
        if self._sensor.state == GpioState.UNKNOWN:
            return 0

        # Emit sound.
        emit_time = time.time()
        self._emitter.state = GpioState.HIGH
        time.sleep(.000015)
        self._emitter.state = GpioState.LOW

        # Wait that the primary wave is not detected anymore.
        while self._sensor.state == GpioState.LOW:
            # Guard against faults.
            if time.time() - emit_time >= 1:
                return -1

        # Measure the time it takes for the reflected sound to return
        while self._sensor.state == GpioState.HIGH:
            # Guard against faults.
            if time.time() - emit_time >= 1:
                return -1

        return_time = time.time()

        # total_distance = time * sound_velocity
        return (return_time - emit_time) * 343 / 2

    async def async_get_distance(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_distance)
