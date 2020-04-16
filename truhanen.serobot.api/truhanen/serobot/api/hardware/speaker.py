
import asyncio as aio
import subprocess
from typing import Optional
import logging
import textwrap


# Module-level logger
logger = logging.getLogger(__name__)


class Speaker:
    """Class for playing sound through a PCM device. To setup a bluetooth
    speaker, see README.md for instructions.
    """
    def __init__(self, device_name: str = 'bluealsa'):
        """
        Parameters
        ----------
        device_name : str
            The name of the PCM device to be used with 'aplay -D {device_name}'.
            The default value 'bluealsa' should be used with a bluetooth
            speaker setup as instructed in README.md.
        """
        self._device_name = device_name

    def shell_command_espeak(
            self, text: str, voice_language: str = 'en-us',
            voice_variant: str = 'm3', amplitude: int = 100,
            pitch: int = 60, speed: int = 150):
        """Form the shell command for speaking some text using the espeak
        synthesizer.

        Parameters
        ----------
        text : str
            The text to be spoken.
        voice_language : str
            The voice language prefix of the espeak voice parameter.
        voice_variant : str
            The voice variant postfix of the espeak voice parameter. For
            example 'm1', 'f4', 'klatt', or 'whisper'.
        amplitude : str
            The espeak amplitude parameter.
        pitch : int
            The espeak pitch parameter.
        speed : int
            The espeak speed parameter.

        Returns
        -------
        shell_command : str
            The shell command for speaking the text through the speaker.
        """
        voice = f'{voice_language}+{voice_variant}'
        shell_command = (
            f'espeak "{text}" -v{voice} -a{amplitude} -p{pitch} -s{speed} '
            f'--stdout | aplay -D {self._device_name}')
        return shell_command

    @staticmethod
    def _check_shell_output(shell_command: str, returncode: int,
                            stdout_data: Optional[bytes] = None,
                            stderr_data: Optional[bytes] = None):
        """Check whether a process completed without problems."""
        def indent(text):
            return textwrap.indent(text, '    ')
        if returncode != 0:
            error_message = f'Shell command "{shell_command!r}" exited with {returncode}'
            if stdout_data:
                error_message += f'\nstdout:\n{indent(stdout_data.decode())}'
            if stderr_data:
                error_message += f'\nstderr:\n{indent(stderr_data.decode())}'
            logger.error(error_message)

    def text_to_speech(self, text: str, **kwargs):
        """Speak some text using this Speaker.

        Parameters
        ----------
        text : str
            The text to be spoken.
        **kwargs : Any
            Keyword arguments to be passed to Speaker.shell_command_espeak()
        """
        shell_command = self.shell_command_espeak(text, **kwargs)
        process = subprocess.run(shell_command, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._check_shell_output(shell_command, process.returncode,
                                 process.stdout, process.stderr)

    async def async_text_to_speech(self, text: str, **kwargs):
        shell_command = self.shell_command_espeak(text, **kwargs)
        process = await aio.create_subprocess_shell(
            shell_command, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        # Wait for the process to terminate.
        stdout_data, stderr_data = await process.communicate()
        self._check_shell_output(shell_command, process.returncode,
                                 stdout_data, stderr_data)
