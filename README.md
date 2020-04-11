# serobot

API & web UI for controlling a Raspberry Pi robot.

### Features
- Support for most of the devices of the development platform, including
    - Robot movement
    - Camera movement & imaging
    - Buzzer
    - RGB leds
- Web server & UI (Python aiohttp & Vue.js)

## Development platform

The package is currently being developed on the following system.

- AlphaBot2-PiZero by Waveshare
    - [Product page](https://www.waveshare.com/product/raspberry-pi/robots/mobile-robots/alphabot2-pizero-w.htm)
    - [Wiki page](https://www.waveshare.com/wiki/AlphaBot2-PiZero)
- Raspberry Pi Zero W
    - [Product page](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- Raspbian GNU/Linux 10 (buster)
- Python 3.7

## Installation

### Python package

1. Clone this project on a Raspberry Pi.
1. Activate a Python 3.7 virtualenv (setup instructions [below](#python-environment-setup)).
1. In the project root directory run `pip install .`

### Web UI

Building the web interface requires Node.js/npm installation ([download page](https://www.npmjs.com/get-npm)), possibly on an external system.

1. In the directory *truhanen/serobot/web/frontend*, run `npm run build`.
1. If on an external system, copy the created dist directory to the respective path on the Raspberry Pi.

## Example

```python
import time
from truhanen.serobot import Serobot

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

Depending on the platform setup & server configuration, the web UI should now be accessible via a web browser at e.g. *http://192.168.1.100* (HTTP, [WLAN access](#ubuntu-pc--wifi-router-setup)) or *https://your.domain.name* ([HTTPS](#secure-https-connection-setup-with-lets-encrypthttpsletsencryptorg), [Internet access](#internet-access)).

## Platform setup

Below are listed some step-by-step instructions for setting up a functional platform with a Ubuntu PC & wifi.

### MicroSD card setup

Use the Raspberry Pi Imager ([download page](https://www.raspberrypi.org/downloads/)) to write a Raspbian OS image on a microSD card.

Optionally give the Raspberry Pi a new hostname by changing the occurrences of the default hostname *raspberrypi* in the files */etc/hostname* and */etc/hosts* on the *rootfs* partition.

#### Wifi connection

Follow the official [instructions](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md). Note, if the wifi device name on your PC is not *wlan0*, check the correct one with `ifconfig`.

#### SSH connection

Create an empty file named *ssh* to the *boot* partition of the SD card.

Optionally restrict to key based SSH authentication as follows.
1. In the file */etc/ssh/ssh_config* on the *rootfs* partition, replace the line `# PasswordAuthentication yes` with` PasswordAuthentication no`.
1. Create a directory */home/pi/.ssh* on the *rootfs* partition with permissions set to *700*.
1. Create a file */home/pi/.ssh/authorized_keys* on the *rootfs* partition.
1. Copy the contents of your own public key file, e.g. *~/.ssh/id_rsa.pub*, to the *authorized_keys* file.
1. Set the permissions of the *authorized_keys* file to *600*.

### Ubuntu PC & wifi router setup

Startup the Raspberry Pi. If setup correctly, the system should now be listed in the settings of your wifi router, under e.g. *DHCP Clients List*.

In the settings of the router, add a reserved IP address, e.g. *192.168.1.100*, for the MAC address of the Raspberry Pi.

To easily connect to the Raspberry Pi from your PC with `ssh pi@raspberrypi`, add the line `192.162.1.100 raspberrypi` (or whatever IP address and hostname you have chosen) to the file */etc/hosts*.

### Raspbian setup

On the Raspberry Pi, run `sudo raspi-config` and enable *Ìnterfacing Options* -> *Camera* and then *Ìnterfacing Options* -> *I2C*.

### Python environment setup

1. On the Raspberry Pi, install Pip with `sudo apt install python3-pip`.
1. Install virtualenvwrapper & dependencies with `pip3 install --user virtualenvwrapper`
1. Setup virtualenvwrapper by adding the following lines to */home/pi/.bashrc* and by running `source .bashrc`.
    ```
    # Virtualenvwrapper settings
    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.7
    export VIRTUALENVWRAPPER_VIRTUALENV=$HOME/.local/bin/virtualenv
    export VIRTUALENVWRAPPER_SCRIPT=$HOME/.local/bin/virtualenvwrapper.sh
    source $VIRTUALENVWRAPPER_SCRIPT
    export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin  # Needed to find the activate script
    ```
1. Create a virtualenv named *serobot* with `mkvirtualenv --python=/usr/bin/python3.7 serobot`.
1. Afterwards, when installing & using Python packages, first activate the virtualenv with `workon serobot`.

### Internet access

To access the Serobot web server from the Internet, you need a domain name and a DNS service, and probably also a dynamic DNS setup.

One DNS service option is provided by [Namecheap](https://www.namecheap.com/), for which a simple DDNS client implementation can be found in [truhanen/ddnsclient](https://github.com/truhanen/ddnsclient).

Depending on whether HTTP or HTTPS is used, forward ports 80 or 443 to the Raspberry Pi from your wifi router settings.

#### Secure HTTPS connection setup with [Let's Encrypt](https://letsencrypt.org)

1. On the Raspberry Pi, install [Certbot](https://certbot.eff.org/) (tool recommended by Let's Encrypt) with `sudo apt install certbot`.
1. In the settings of your wifi router, forward HTTP port 80, at least temporarily, to the Raspberry Pi.
1. Run `sudo certbot certonly --standalone` and list the domains you want to get certificates for.

Now you should have two certificate *.pem* files in */etc/letsencrypt/live/[domain.name]/*.

To keep the certificates renewed before they expire, keep the port 80 forwarded, and start the renewal background service with `sudo certbot renew`.
