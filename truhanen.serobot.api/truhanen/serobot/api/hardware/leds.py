
from enum import Enum
import asyncio as aio
import logging

try:
    import rpi_ws281x
except ModuleNotFoundError:
    rpi_ws281x = None

from .bcm_channel import BcmChannel


# Module-level logger
logger = logging.getLogger(__name__)


class RgbValue(Enum):
    NONE    = (  0,   0,   0)
    WHITE   = (255, 255, 255)
    RED     = (255,   0,   0)
    GREEN   = (  0, 255,   0)
    BLUE    = (  0,   0, 255)
    YELLOW  = (255, 255,   0)
    MAGENTA = (255,   0, 255)
    CYAN    = (  0, 255, 255)


class Leds:
    led_count = 4
    dma = 10  # DMA channel
    default_on_brightness = 50

    def __init__(self):
        self._brightness = None
        self._rgb_values = [None] * self.led_count

        # Initialize the LED interface.
        failed_message = 'The Leds instance will have no physical functionality.'
        if rpi_ws281x is not None:
            try:
                self._leds = rpi_ws281x.PixelStrip(
                    self.led_count, BcmChannel.leds, dma=self.dma)
                self._leds.begin()
            except RuntimeError:
                logger.warning(
                    'Could not initialize rpi_ws281.PixelStrip. You may have '
                    'to run as root. ' + failed_message)
                self._leds = None
        else:
            logger.warning('Module rpi_ws281x is missing. ' + failed_message)
            self._leds = None

        self.brightness = 0
        self.rgb = RgbValue.WHITE
        self.show()

    def __del__(self):
        self.brightness = 0
        self.show()

    def show(self):
        """Apply the changes made by the set methods."""
        if self._leds is not None:
            self._leds.show()
        else:
            logger.info('Leds not fully initialized. Display not physically updated.')

    @property
    def rgb(self):
        """
        Returns
        -------
        rgb : List[tuple]
            RGB values of the LEDs, from the rightmost to the leftmost.
        """
        return self._rgb_values.copy()

    @rgb.setter
    def rgb(self, value):
        """
        Parameters
        ----------
        value : RgbValue | tuple | List[RgbValue] | List[tuple]
            The RGB value(s) to be set to the LEDs. Tuple values should contain
            three integers in the range 0-255. If a list is given, it should
            contain four values, one for each LED, from the rightmost to the
            leftmost.
        """
        # Broadcast if a single value is given.
        if isinstance(value, RgbValue):
            value = [value] * self.led_count
        elif isinstance(value, tuple):
            value = [value] * self.led_count

        # Convert RgbValues to tuples.
        value = [v.value if isinstance(v, RgbValue) else v for v in value]

        # Set values.
        for position, rgb in enumerate(value):
            if self._leds is not None:
                self._leds.setPixelColorRGB(position, *rgb)
            self._rgb_values[position] = rgb
        if self._leds is None:
            logger.info('Leds not fully initialized. RGB not physically changed.')

    @property
    def brightness(self):
        """
        Returns
        -------
        brightness : int
            The brightness value of the LEDs.
        """
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        """
        Parameters
        ----------
        value : int
            Brightness value of the LEDs. Value range 0-255.
        """
        if self._leds is not None:
            self._leds.setBrightness(value)
        else:
            logger.info('Leds not fully initialized. Brightness not physically '
                        'changed.')
        self._brightness = value

    @property
    def on(self):
        return self.brightness > 0

    @on.setter
    def on(self, value):
        if value:
            self.brightness = self.default_on_brightness
        else:
            self.brightness = 0

    async def async_show(self):
        return await aio.get_running_loop().run_in_executor(None, self.show)

    async def async_set_rgb(self, value):
        await aio.get_running_loop().run_in_executor(
            None, setattr, self, 'rgb', value)
        return await self.async_show()

    async def async_set_brightness(self, value):
        await aio.get_running_loop().run_in_executor(
            None, setattr, self, 'brightness', value)
        return await self.async_show()

    async def async_set_on(self, value):
        await aio.get_running_loop().run_in_executor(
            None, setattr, self, 'on', value)
        return await self.async_show()
