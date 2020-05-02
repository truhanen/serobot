
from enum import IntEnum, auto
import logging
from typing import Optional, List

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    GPIO = None

from .bcm_channel import BcmChannel


class GpioDirection(IntEnum):
    IN = GPIO.IN if GPIO is not None else auto()
    OUT = GPIO.OUT if GPIO is not None else auto()


class GpioState(IntEnum):
    HIGH = GPIO.HIGH if GPIO is not None else auto()
    LOW = GPIO.LOW if GPIO is not None else auto()
    # This tells e.g. that a GPIO state could not be read.
    UNKNOWN = auto()


class GpioPull(IntEnum):
    OFF = GPIO.PUD_OFF if GPIO is not None else auto()
    DOWN = GPIO.PUD_DOWN if GPIO is not None else auto()
    UP = GPIO.PUD_UP if GPIO is not None else auto()


# Module-level logger
logger = logging.getLogger(__name__)


if GPIO is not None:
    # Set general settings whenever the GpioDevice class is used.
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
else:
    logger.warning('Module RPi.GPIO is missing. General GPIO settings were '
                   'not applied.')


class GpioSetup:
    """Class for managing a general GPIO channel, input, output, or PWM."""
    def __init__(self, bcm_channel: BcmChannel,
                 direction: GpioDirection,
                 pull: Optional[GpioPull] = None,
                 initial: Optional[GpioState] = None):
        self._channel = bcm_channel
        if GPIO is not None:
            # Create kwargs without None values.
            kwargs = dict(direction=direction)
            if pull is not None:
                kwargs['pull_up_down'] = pull
            if initial is not None:
                kwargs['initial'] = initial
            GPIO.setup(bcm_channel, **kwargs)
        else:
            logger.warning(f'Module RPi.GPIO is missing. Did not really '
                           f'setup {bcm_channel!r}.')

    def __del__(self):
        if GPIO is not None:
            GPIO.cleanup(self.channel)
        else:
            logger.warning(f'Module RPi.GPIO is missing. Did not really '
                           f'cleanup {self.channel!r}.')

    @property
    def channel(self):
        return self._channel


class GpioInput(GpioSetup):
    """Class for managing a GPIO input channel."""
    def __init__(self, bcm_channel: BcmChannel, pull: Optional[GpioPull] = None):
        super().__init__(bcm_channel, direction=GpioDirection.IN, pull=pull)

    @property
    def state(self) -> GpioState:
        """The state of the GPIO input pin."""
        if GPIO is not None:
            state = GpioState(GPIO.input(self.channel))
        else:
            logger.info(f'Module RPi.GPIO is missing. Did not really read '
                        f'the state of {self.channel!r}.')
            state = GpioState.UNKNOWN
        return state


class GpioOutput(GpioSetup):
    """Class for managing a GPIO output channel."""
    def __init__(self, bcm_channel: BcmChannel, initial: Optional[GpioState] = None):
        super().__init__(bcm_channel, direction=GpioDirection.OUT, initial=initial)

    @property
    def state(self) -> GpioState:
        """The state of the GPIO output pin."""
        if GPIO is not None:
            state = GpioState(GPIO.input(self.channel))
        else:
            logger.info(f'Module RPi.GPIO is missing. Did not really read '
                        f'the state of {self.channel!r}.')
            state = GpioState.UNKNOWN
        return state

    @state.setter
    def state(self, value: GpioState):
        if GPIO is not None:
            GPIO.output(self.channel, value)
        else:
            logger.info(f'Module RPi.GPIO is missing. Did not physically change '
                        f'the state of {self.channel!r}.')

    @classmethod
    def set_multiple(cls, outputs: List['GpioOutput'], states: List[GpioState]):
        """Set the states of multiple GPIO outputs with a single call."""
        channels = [output.channel for output in outputs]
        if GPIO is not None:
            GPIO.output(channels, states)
        else:
            logger.info(f'Module RPi.GPIO is missing. Did not physically change '
                        f'the states of {channels!r}.')


class GpioPwm(GpioSetup):
    """Class for managing a GPIO PWM channel."""
    def __init__(self, bcm_channel: BcmChannel,
                 initial: Optional[GpioState] = None,
                 frequency: int = 1,
                 duty_cycle: int = 100):
        """
        Parameters
        ----------
        bcm_channel
            The GPIO channel of the PWM.
        initial
            Initial state of the GPIO channel.
        frequency
            The initial frequency of the PWM, in Hertz.
        duty_cycle
            The initial duty cycle of the PWM, as percentage.
        """
        super().__init__(bcm_channel, direction=GpioDirection.OUT, initial=initial)
        self._frequency = frequency
        self._duty_cycle = duty_cycle
        if GPIO is not None:
            self._pwm = GPIO.PWM(self.channel, frequency)
        else:
            logger.warning(f'Module RPi.GPIO is missing. Did not really '
                           f'setup the PWM for {bcm_channel!r}.')
            self._pwm = None

    @property
    def frequency(self) -> float:
        return self._frequency

    @frequency.setter
    def frequency(self, value: float):
        self._frequency = value
        if self._pwm is not None:
            self._pwm.ChangeFrequency(value)
        else:
            logger.info(f'The PWM instance is missing. Did not physically change '
                        f'the frequency of the PWM in {self.channel!r}.')

    @property
    def duty_cycle(self) -> float:
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value: float):
        self._duty_cycle = value
        if self._pwm is not None:
            self._pwm.ChangeDutyCycle(value)
        else:
            logger.info(f'The PWM instance is missing. Did not physically change '
                        f'the duty cycle of the PWM in {self.channel!r}.')

    def start(self):
        if self._pwm is not None:
            self._pwm.start(self.duty_cycle)
        else:
            logger.info(f'The PWM instance is missing. Did not physically '
                        f'start the PWM in {self.channel!r}.')

    def stop(self):
        if self._pwm is not None:
            self._pwm.stop()
        else:
            logger.info(f'The PWM instance is missing. Did not physically '
                        f'stop the PWM in {self.channel!r}.')
