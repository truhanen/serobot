
import asyncio as aio

from .bcm_channel import BcmChannel
from .gpio import GpioOutput, GpioState


class Buzzer:
    def __init__(self):
        self._output = GpioOutput(BcmChannel.buzzer, initial=GpioState.LOW)
        self._on = False

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, value):
        """
        Parameters
        ----------
        value : bool
            The state of the buzzer.
        """
        self._on = value
        self._output.state = GpioState.HIGH if value else GpioState.LOW

    async def async_on(self, duration=.05):
        """Set the buzzer on for a period of time.

        Parameters
        ----------
        duration : Number
            The duration that the buzzer will be on, in seconds.
        """
        self.on = True
        await aio.sleep(duration)
        self.on = False
