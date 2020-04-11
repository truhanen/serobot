
from abc import ABC, abstractmethod
import asyncio as aio
from typing import Dict, Any


class AbstractHardwareCommand(ABC):
    def __init__(self, bot: 'serobot.Serobot'):
        self._bot = bot

    @property
    def bot(self):
        return self._bot

    @abstractmethod
    async def command(self, parameters: Any):
        """Perform the command of this instance.

        Parameters
        ----------
        parameters : Any
            Possible command parameters as received from the web frontend.
        """
        pass


class CameraPanCommand(AbstractHardwareCommand):
    delta_map = dict(left=100, right=-100)

    async def command(self, direction: str):
        """
        Parameters
        ----------
        direction : 'left' | 'right'
        """
        delta = self.delta_map[direction]
        aio.create_task(self.bot.camera.async_set_pan_value(
            self.bot.camera.pan_value + delta))


class CameraTiltCommand(AbstractHardwareCommand):
    delta_map = dict(up=-100, down=100)

    async def command(self, direction: str):
        """
        Parameters
        ----------
        direction : 'up' | 'down'
        """
        delta = self.delta_map[direction]
        aio.create_task(self.bot.camera.async_set_tilt_value(
            self.bot.camera.tilt_value + delta))


class CameraCenterCommand(AbstractHardwareCommand):
    async def command(self, _):
        aio.create_task(self.bot.camera.async_set_to_center())


class RebootCommand(AbstractHardwareCommand):
    async def command(self, _):
        self.bot.rpi.reboot()


class MotorCommand(AbstractHardwareCommand):
    async def command(self, function_name):
        """
        Parameters
        ----------
        function_name : str
            The name of the method to be called on self.bot.motors
        """
        getattr(self.bot.motors, function_name)()


class BuzzerCommand(AbstractHardwareCommand):
    async def command(self, on: bool):
        """
        Parameters
        ----------
        on : bool
            The 'on' state to be set on self.bot.buzzer
        """
        self.bot.buzzer.on = on


class LedRgbCommand(AbstractHardwareCommand):
    async def command(self, rgb_dict: Dict[str, int]):
        """
        Parameters
        ----------
        rgb_dict : Dict[str, int]
            Dictionary of rgb values, with keys 'red', 'green', & 'blue'.
            Values range between 0-255.
        """
        rgb_tuple = tuple(rgb_dict[key] for key in ['red', 'green', 'blue'])
        aio.create_task(self.bot.leds.async_set_rgb(rgb_tuple))


class LedBrightnessCommand(AbstractHardwareCommand):
    async def command(self, brightness: int):
        """
        Parameters
        ----------
        brightness : int
            The brightness value to be set on self.bot.leds. Value range 0-255.
        """
        aio.create_task(self.bot.leds.async_set_brightness(brightness))


class HardwareCommander:
    """Collection class for the different AbstractHardwareCommand types.
    Used for handling command messages received from the web frontend.
    """
    def __init__(self, bot: 'serobot.Serobot'):
        self._bot = bot
        self._commands = dict(
            camera_pan=CameraPanCommand(self.bot),
            camera_tilt=CameraTiltCommand(self.bot),
            camera_center=CameraCenterCommand(self.bot),
            reboot=RebootCommand(self.bot),
            motors=MotorCommand(self.bot),
            buzzer=BuzzerCommand(self.bot),
            led_rgb=LedRgbCommand(self.bot),
            led_brightness=LedBrightnessCommand(self.bot),
        )

    @property
    def bot(self):
        return self._bot

    @property
    def commands(self):
        return self._commands

    async def command(self, commands: Dict[str, Any]):
        """
        Parameters
        ----------
        commands : Dict[str, Any]
            Command message as received from the web frontend.

            Mapping from command names to parameters to be passed to the
            commands. Possible keys are the keys of self.commands, and values
            are the parameters to be passed to the command() method of the
            respective AbstractHardwareCommand subclass instance.

        Returns
        -------
        unconsumed_commands : Dict[str, Any]
            Commands that could not be performed.
        """
        unconsumed_commands = dict()
        for command_name, parameters in commands.items():
            if command_name in self.commands:
                await self.commands[command_name].command(parameters)
            else:
                unconsumed_commands[command_name] = parameters
        return unconsumed_commands
