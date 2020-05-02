
import asyncio as aio
from dataclasses import dataclass
from typing import List

from .hardware import(
    RaspberryPi,
    Camera,
    Motors,
    Leds,
    Buzzer,
    RCReceiver,
    DistanceSensor,
    LineTrackers,
    ProximitySensors,
    Speaker,
)


@dataclass
class SerobotStatus:
    cpu_load:              float
    distance_sensor_value: float
    left_proximity_value:  bool
    right_proximity_value: bool
    line_tracker_values:   List[int]
    led_brightness:        int
    buzzer_on:             bool
    camera_exposure:       int


class Serobot:
    def __init__(self):
        self._rpi = RaspberryPi()
        self._camera = Camera()
        self._motors = Motors()
        self._leds = Leds()
        self._buzzer = Buzzer()
        self._rc_receiver = RCReceiver()
        self._distance_sensor = DistanceSensor()
        self._line_trackers = LineTrackers()
        self._proximity_sensors = ProximitySensors()
        self._speaker = Speaker()

    @property
    def rpi(self):
        return self._rpi

    @property
    def camera(self):
        return self._camera

    @property
    def motors(self):
        return self._motors

    @property
    def buzzer(self):
        return self._buzzer

    @property
    def leds(self):
        return self._leds

    @property
    def rc_receiver(self):
        return self._rc_receiver

    @property
    def distance_sensor(self):
        return self._distance_sensor

    @property
    def line_trackers(self):
        return self._line_trackers

    @property
    def proximity_sensors(self):
        return self._proximity_sensors

    @property
    def speaker(self):
        return self._speaker

    async def get_status(self) -> SerobotStatus:
        status = list(await aio.gather(
            self.rpi.async_get_cpu_load(),
            self.distance_sensor.async_get_distance(),
            self.proximity_sensors.async_get_left_proximity(),
            self.proximity_sensors.async_get_right_proximity(),
            self.line_trackers.async_read_analog_values()
        ))
        status.extend([self.leds.brightness,
                       self.buzzer.on,
                       self.camera.camera.exposure_speed])

        return SerobotStatus(*status)
