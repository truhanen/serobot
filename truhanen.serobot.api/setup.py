
from setuptools import setup, find_namespace_packages


setup(
    name='truhanen.serobot.api',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    description='API for controlling a Raspberry Pi robot.',
    install_requires=[
        'psutil',
        'smbus',
        'RPi.GPIO',
        'picamera',
        'rpi-ws281x',
    ],
    packages=find_namespace_packages(),
    zip_safe=False,
)
