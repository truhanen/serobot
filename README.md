# serobot

API & web UI for controlling a Raspberry Pi robot.

### Features
- Support for most of the devices of the development platform, including
    - Robot movement
    - Camera movement & imaging
    - Buzzer
    - RGB leds
- Web server & UI, Python aiohttp & Vue.js

## Development platform

The package is currently being developed on the following system.

- AlphaBot2-PiZero by Waveshare
    - [Product page](https://www.waveshare.com/product/raspberry-pi/robots/mobile-robots/alphabot2-pizero-w.htm)
    - [Wiki page](https://www.waveshare.com/wiki/AlphaBot2-PiZero)
- Raspberry Pi Zero W
    - [Product page](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- Raspbian GNU/Linux 9 (stretch)
- Python 3.7

## Installation

### Python package

In the project root directory, run
```
pip install --user .
```

### Web UI

Building the web interface requires Node.js/npm installation. (Possibly on an external system.)
- [Node.js/npm download page](https://www.npmjs.com/get-npm)

In the directory serobot/web/frontend, run
```
npm run build
```
(If on an external system, copy the created dist directory to the respective path on the Raspberry Pi.)

## Example

```python
import time
from serobot import Serobot

bot = Serobot()

# Movement
bot.motors.move_forward()
time.sleep(.5)
bot.motors.turn_right()
time.sleep(1)
bot.motors.stop()
# asyncio
await bot.motors.async_move_forward(.5)
await bot.motors.async_turn_right(1)

# Camera
bot.camera.pan_value = 100
bot.camera.tilt_value = 100
bot.camera.take_picture('figure.jpg')
# asyncio
await bot.camera.async_set_pan_value(100)
await bot.camera.async_set_tilt_value(100)
await bot.camera.async_take_picture('figure.jpg')
```

## Web server/UI configuration & usage

Use the installed script `start_serobot_server`,
```
pi@raspberrypi:~ $ start_serobot_server --help
usage: start_serobot_server [-h] [-a AUTH_FILE] [-c SSL_CERTFILE]
                            [-k SSL_KEYFILE]
                            [config_file]

positional arguments:
  config_file           A configuration file listing the other arguments as

                        [config]
                        auth_file = /path/to/auth/file
                        ssl_certfile = /path/to/ssl/certfile
                        ssl_keyfile = /path/to/ssl/keyfile

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH_FILE, --auth-file AUTH_FILE
                        A file that lists the authorized usernames and
                        passwords. The file must contain sections of the form

                        [myusername]
                        password = mypassword
  -c SSL_CERTFILE, --ssl-certfile SSL_CERTFILE
                        Path to a certificate file for SSL, .pem
  -k SSL_KEYFILE, --ssl-keyfile SSL_KEYFILE
                        Path to a key file for SSL, .pem
```
