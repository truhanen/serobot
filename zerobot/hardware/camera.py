
from functools import partial
import asyncio as aio

from ._pca import PCA  # PCA9685 driver from the AlphaBot2 demo package
from picamera import PiCamera


class Camera:
    # I2C address of the camera pan/tilt control
    i2c_camera_servo_address = 0x40

    pan_center_value = 1500  # Greater value is more left
    tilt_center_value = 1600  # Greater value is more down
    pan_min_value = 1000  # Was 600
    pan_max_value = 2000  # Was 2400
    tilt_min_value = 1000  # Was 700
    tilt_max_value = 2000  # Was 2000

    def __init__(self):
        # These will be initialized by the setters
        self._pan_value = None
        self._tilt_value = None
        self._pwm = PCA(self.i2c_camera_servo_address)

        # Setup camera.
        # Resolution 1640x1232, 4:3, full FOV, 2x2 binning
        # Use low framerate for better low-light images
        self._camera = PiCamera(resolution=(1640, 1232), framerate=5)
        self._camera.exposure_mode = 'night'
        # self._camera.shutter_speed = 1000000
        # self._camera.exposure_compensation = 25
        # self._camera.iso = 800

        self._camera.start_preview()
        self.pan_value = self.pan_center_value
        self.tilt_value = self.tilt_center_value

    def __del__(self):
        self.set_to_center()

    @property
    def camera(self):
        return self._camera

    @property
    def pan_value(self):
        """
        Returns
        -------
        Camera left/right position. Greater value is more left. Center is 1500.
        """
        return self._pan_value

    @pan_value.setter
    def pan_value(self, value):
        value = max(min(value, self.pan_max_value), self.pan_min_value)
        self._pan_value = value
        self._pwm.set_servo_pulse(0, value)

    @property
    def tilt_value(self):
        """
        Returns
        -------
        Camera up/down position. Greater value is more down. Center is 1500.
        """
        return self._tilt_value

    @tilt_value.setter
    def tilt_value(self, value):
        value = max(min(value, self.tilt_max_value), self.tilt_min_value)
        self._tilt_value = value
        self._pwm.set_servo_pulse(1, value)

    def set_to_center(self):
        self.pan_value = self.pan_center_value
        self.tilt_value = self.tilt_center_value

    def take_picture(self, output, **kwargs):
        """Take a picture with the camera"""
        return self._camera.capture(output, **kwargs)

    async def async_set_pan_value(self, value):
        return await aio.get_running_loop().run_in_executor(
            None, setattr, self, 'pan_value', value)

    async def async_set_tilt_value(self, value):
        return await aio.get_running_loop().run_in_executor(
            None, setattr, self, 'tilt_value', value)

    async def async_set_to_center(self):
        return await aio.get_running_loop().run_in_executor(
            None, self.set_to_center)

    async def async_take_picture(self, *args, **kwargs):
        return await aio.get_running_loop().run_in_executor(
            None, partial(self.take_picture, *args, **kwargs))
