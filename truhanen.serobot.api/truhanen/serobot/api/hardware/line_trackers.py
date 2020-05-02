
import time
import asyncio as aio

from .bcm_channel import BcmChannel
from .gpio import GpioOutput, GpioInput, GpioState, GpioPull


class LineTrackers:
    tracker_count = 5

    def __init__(self):
        self._conversation_output = GpioOutput(BcmChannel.line_trackers_conversation)
        self._address_output = GpioOutput(BcmChannel.line_trackers_address, initial=GpioState.LOW)
        self._clock_output = GpioOutput(BcmChannel.line_trackers_clock, initial=GpioState.LOW)
        self._sensors_input = GpioInput(BcmChannel.line_trackers_sensors, pull=GpioPull.UP)

    def read_analog_values(self):
        if self._sensors_input.state == GpioState.UNKNOWN:
            return None

        value = [0] * (self.tracker_count + 1)
        for i in range(len(value)):
            # Trigger conversation.
            self._conversation_output.state = GpioState.LOW

            for j in range(4):
                # Transfer channel address on clock 0 to 4.
                if (i >> (3 - j)) & 0x01:
                    self._address_output.state = GpioState.HIGH
                else:
                    self._address_output.state = GpioState.LOW

                # Receive the first 4 bits of the previous conversion result.
                value[i] <<= 1
                if self._sensors_input.state == GpioState.HIGH:
                    value[i] |= 0x01

                self._clock_output.state = GpioState.HIGH
                self._clock_output.state = GpioState.LOW

            # Receive the last 6 bits of the previous conversation result.
            for j in range(6):
                value[i] <<= 1
                if self._sensors_input.state == GpioState.HIGH:
                    value[i] |= 0x01

                self._clock_output.state = GpioState.HIGH
                self._clock_output.state = GpioState.LOW

            time.sleep(.0001)
            self._conversation_output.state = GpioState.HIGH

        return value[1:]

    async def async_read_analog_values(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.read_analog_values)
