
from setuptools import setup


# TODO Optionally build the web frontend?


setup(
    name='serobot',
    version='0.1.0',
    author='Tuukka Ruhanen',
    author_email='tuukka.t.ruhanen@gmail.com',
    install_requires=[
        # Hardware control
        'psutil',
        'RPi.GPIO',
        'picamera',
        'rpi-ws281x',
        # Web server
        'aiohttp',
        'aiohttp_security',
        'aiohttp_session',
        'cryptography',
    ],
    packages=[
        'serobot',
        'serobot.hardware',
        'serobot.web',
    ],
    scripts=[
        'scripts/start_serobot_server',
    ],
    zip_safe=False,
)
