
import time
import asyncio as aio

import RPi.GPIO as GPIO

from ._pin_numbers import (
    bcm_ultrasonic_sensor,
    bcm_ultrasonic_emitter
)


class DistanceSensor:
    def __init__(self):
        GPIO.setup(bcm_ultrasonic_emitter, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(bcm_ultrasonic_sensor, GPIO.IN)

    def get_distance(self):
        """Get distance in meters.

        Note that this Python implementation may be rather unreliable.
        """
        # Emit sound.
        emit_time = time.time()
        GPIO.output(bcm_ultrasonic_emitter, GPIO.HIGH)
        time.sleep(.000015)
        GPIO.output(bcm_ultrasonic_emitter, GPIO.LOW)

        # Wait that the primary wave is not detected anymore.
        while not GPIO.input(bcm_ultrasonic_sensor):
            # Guard against faults.
            if time.time() - emit_time >= 1:
                return -1

        # Measure the time it takes for the reflected sound to return
        while GPIO.input(bcm_ultrasonic_sensor):
            # Guard against faults.
            if time.time() - emit_time >= 1:
                return -1

        return_time = time.time()

        # total_distance = time * sound_velocity
        return (return_time - emit_time) * 343 / 2

    async def async_get_distance(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.get_distance)
