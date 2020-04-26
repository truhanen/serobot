
from setuptools import setup, find_namespace_packages


def is_current_system_raspberry_pi():
    """Determine whether the current system is a Raspberry Pi.

    Use the same method that is used by the setup script of
    the picamera package. Namely search for the entry 'Hardware'
    in /proc/cpuinfo.
    """
    is_raspberry_pi = False
    with open('/proc/cpuinfo', 'r') as cpuinfo:
        for line in cpuinfo:
            if line.startswith('Hardware'):
                label, value = line.strip().split(':', 1)
                value = value.strip()
                if value in ('BCM2708', 'BCM2709', 'BCM2835', 'BCM2836'):
                    is_raspberry_pi = True
    return is_raspberry_pi


install_requires = [
    'psutil',
    'smbus',
]
# Install the following packages only if on an actual Raspberry Pi system.
if is_current_system_raspberry_pi():
    install_requires.extend(['RPi.GPIO', 'picamera', 'rpi-ws281x'])


setup(
    name='truhanen.serobot.api',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    description='API for controlling a Raspberry Pi robot.',
    install_requires=install_requires,
    packages=find_namespace_packages(),
    zip_safe=False,
)
