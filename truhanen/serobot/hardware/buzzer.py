
import asyncio as aio

import RPi.GPIO as GPIO

from ._pin_numbers import bcm_buzz


class Buzzer:
    def __init__(self):
        GPIO.setup(bcm_buzz, GPIO.OUT, initial=GPIO.LOW)
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
        if value:
            GPIO.output(bcm_buzz, GPIO.HIGH)
        else:
            GPIO.output(bcm_buzz, GPIO.LOW)
        self._on = value

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
