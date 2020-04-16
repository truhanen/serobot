
import time
import asyncio as aio

import RPi.GPIO as GPIO

from ._pin_numbers import (
    bcm_ir_tracker_cs,
    bcm_ir_tracker_sensors,
    bcm_ir_tracker_address,
    bcm_ir_tracker_clock
)


class LineTrackers:
    tracker_count = 5

    def __init__(self):
        GPIO.setup(bcm_ir_tracker_cs, GPIO.OUT)
        GPIO.setup(bcm_ir_tracker_address, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(bcm_ir_tracker_clock, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(bcm_ir_tracker_sensors, GPIO.IN, GPIO.PUD_UP)

    def read_analog_values(self):
        value = [0] * (self.tracker_count + 1)
        for i in range(len(value)):
            # Trigger conversation
            GPIO.output(bcm_ir_tracker_cs, GPIO.LOW)

            for j in range(4):
                # Transfer channel address on clock 0 to 4
                if (i >> (3 - j)) & 0x01:
                    GPIO.output(bcm_ir_tracker_address, GPIO.HIGH)
                else:
                    GPIO.output(bcm_ir_tracker_address, GPIO.LOW)

                # Receive the first 4 bits of the previous conversion result
                value[i] <<= 1
                if GPIO.input(bcm_ir_tracker_sensors):
                    value[i] |= 0x01

                GPIO.output(bcm_ir_tracker_clock, GPIO.HIGH)
                GPIO.output(bcm_ir_tracker_clock, GPIO.LOW)

            # Receive the last 6 bits of the previous conversation result
            for j in range(6):
                value[i] <<= 1
                if GPIO.input(bcm_ir_tracker_sensors):
                    value[i] |= 0x01

                GPIO.output(bcm_ir_tracker_clock, GPIO.HIGH)
                GPIO.output(bcm_ir_tracker_clock, GPIO.LOW)

            time.sleep(.0001)
            GPIO.output(bcm_ir_tracker_cs, GPIO.HIGH)

        return value[1:]

    async def async_read_analog_values(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.read_analog_values)
