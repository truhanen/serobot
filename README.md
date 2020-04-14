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
1. If on an external system, copy the created *dist* directory to the respective path on the Raspberry Pi.

## API example

```python
import time
import asyncio as aio

from truhanen.serobot import Serobot

bot = Serobot()

# Movement
bot.motors.move_forward()
time.sleep(.5)
bot.motors.turn_right()
time.sleep(1)
bot.motors.stop()

# Camera
bot.camera.pan_value = 100
bot.camera.tilt_value = 100
bot.camera.take_picture('figure.jpg')

# Do the same actions concurrently with awaitable methods.
async def act():
    await aio.gather(
        # Movement
        bot.motors.async_move_forward(.5),
        bot.motors.async_turn_right(1),
        # Camera
        bot.camera.async_set_pan_value(100),
        bot.camera.async_set_tilt_value(100),
        bot.camera.async_take_picture('figure.jpg'),
    )
aio.run(act())
```

## Web server/UI configuration & usage

### User authentication

For the web server to work, you need to list the authorized users in a file of the form

```
# Username as the section header
[myusername]
# Password of the user
password = mypassword

# Another authorized user
[myusername2]
password = mypassword2
```

### Usage

The web server can now be started with the installed script,

```
pi@raspberrypi:~ $ sudo .virtualenvs/serobot/bin/start_serobot_server -a authorized_users.conf
```

In case of HTTPS (setup instructions [below](#secure-https-connection-with-lets-encrypthttpsletsencryptorg)), give the certificate files as additional arguments to the script, or give a single path argument pointing to a configuration file of the form

```
[config]
auth_file = /path/to/auth/file
ssl_certfile = /path/to/ssl/certfile
ssl_keyfile = /path/to/ssl/keyfile
```

The web UI should now be accessible via a web browser at e.g. *http\://192.168.1.100* (HTTP, [LAN access](#ubuntu-pc--wifi-router-setup)) or *https\://your.domain.name* ([HTTPS](#secure-https-connection-setup-with-lets-encrypthttpsletsencryptorg), [Internet access](#internet-access)).

#### Running without root privileges

Root privileges are needed by the [rpi-ws281x library](https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/library/README.rst) that controls the RGB leds (see [issue](https://github.com/rpi-ws281x/rpi-ws281x-python/issues/9)), and for reading the certificate files for HTTPS. If those features are not needed, the web server can be started also without `sudo`.

## Platform setup

Below are listed some step-by-step instructions for setting up a functional platform with a Ubuntu PC & wifi.

### SD card setup

Use the Raspberry Pi Imager ([download page](https://www.raspberrypi.org/downloads/)) to write a Raspbian OS image on a microSD card.

Optionally give the Raspberry Pi a new hostname by changing the occurrences of the default hostname *raspberrypi* in the files */etc/hostname* and */etc/hosts* on the *rootfs* partition.

#### Wifi connection

Follow the official [instructions](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md). Note, if the wifi device name on your PC is not *wlan0*, check the correct one with `ifconfig`.

#### SSH connection

Create an empty file named *ssh* to the *boot* partition of the SD card.

Optionally restrict to key based SSH authentication as follows.
1. In the file */etc/ssh/ssh_config* on the *rootfs* partition, replace the line `# PasswordAuthentication yes` with `PasswordAuthentication no`.
1. Create a directory */home/pi/.ssh* on the *rootfs* partition with permissions set to *700*.
1. Create a file */home/pi/.ssh/authorized_keys* on the *rootfs* partition.
1. Copy the contents of your own public key file, e.g. *~/.ssh/id_rsa.pub*, to the *authorized_keys* file.
1. Set the permissions of the *authorized_keys* file to *600*.

### Ubuntu PC & wifi router setup

Startup the Raspberry Pi. If setup correctly, the system should now be listed in the settings of your wifi router, under e.g. *DHCP Clients List*.

In the settings of the router, add a reserved IP address, e.g. *192.168.1.100*, for the MAC address of the Raspberry Pi.

To easily connect to the Raspberry Pi from your PC with `ssh pi@raspberrypi`, add the line `192.162.1.100 raspberrypi` (or whatever IP address and hostname you have chosen) to the file */etc/hosts* on your PC.

### Raspbian setup

On the Raspberry Pi, run `sudo raspi-config` and enable *Interfacing Options* -> *Camera* and then *Interfacing Options* -> *I2C*.

### Python environment setup

1. On the Raspberry Pi, install pip with `sudo apt install python3-pip`.
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

To access the Serobot web UI from the Internet, you need a domain name and a DNS service, and probably also a dynamic DNS setup.

One DNS service option is provided by [Namecheap](https://www.namecheap.com/), for which a simple DDNS client implementation can be found in [truhanen/ddnsclient](https://github.com/truhanen/ddnsclient).

Depending on whether HTTP or HTTPS is used, forward ports 80 or 443 to the Raspberry Pi from your wifi router settings.

#### Secure HTTPS connection with [Let's Encrypt](https://letsencrypt.org)

1. On the Raspberry Pi, install [Certbot](https://certbot.eff.org/) (tool recommended by Let's Encrypt) with `sudo apt install certbot`.
1. In the settings of your wifi router, forward HTTP port 80, at least temporarily, to the Raspberry Pi.
1. Run `sudo certbot certonly --standalone` and list the domains you want to get certificates for.

Now you should have two certificate *.pem* files in */etc/letsencrypt/live/[domain.name]/*.

To keep the certificates renewed before they expire, keep the port 80 forwarded, and start the renewal background service with `sudo certbot renew`.

### Playing sound & text-to-speech through a bluetooth speaker

This feature is not yet included in this project, but here are some configuration instructions & command line usage examples for the Raspberry Pi Zero W.

#### Connecting to a bluetooth speaker 

1. Install [Bluetooth ALSA Audio backend](https://github.com/Arkq/bluez-alsa) with `sudo apt install bluealsa`.
1. Start the backend service with `sudo service bluealsa start`.
1. Make your bluetooth speaker discoverable.
1. Start the interactive bluetooth control tool with `sudo bluetoothctl`.
    - Start scanning for devices with `scan on`.
    - List found bluetooth devices with `devices`.
    - When the bluetooth speaker is found, pair and connect to it with commands `pair X`, `trust X`, and `connect X`, where `X` is the MAC address of the device, such as *04:FE:A1:99:4E:A8*.
    - Exit with `exit`.
1. To configure the bluealsa virtual PCM device, create file *~/.asoundrc* with contents
    ```
    defaults.bluealsa.interface "hci0"
    defaults.bluealsa.device "X"
    defaults.bluealsa.profile "a2dp"
    defaults.bluealsa.delay 10000
    ```
    where `X` is again the MAC address of the bluetooth speaker.
1. Try to play sound with the bluealsa device with
    ```
    aplay -D bluealsa /usr/share/sounds/alsa/Front_Center.wav
    ```
1. Later, to disconnect or connect again to the bluetooth speaker, use commands
    ```
    echo -e 'connect X\nexit\n' | sudo bluetoothctl
    echo -e 'disconnect X\nexit\n' | sudo bluetoothctl
    ```
    where `X` is the MAC address of the bluetooth speaker.

#### Text-to-speech

Below are some installation instructions and simple usage examples for two alternative text-to-speech synthesizers.

##### [Espeak](http://espeak.sourceforge.net/)

Install with `sudo apt install espeak`.

Speak through the bluealsa device with
```
espeak "Hello. I am a Raspberry Pi." -ven-us+f3 -p40 -s120 --stdout | aplay -D bluealsa
```

##### [SVOX Pico](https://packages.debian.org/buster/libttspico0)

SVOX Pico may sound more natural than espeak, but also less clear in some cases.

The required packages [are not available](https://bugs.launchpad.net/raspbian/+bug/1835974) in the repositories for Raspbian 10 (buster), but can be downloaded from archives.raspberrypi.org and installed manually with
```
wget http://archive.raspberrypi.org/debian/pool/main/s/svox/libttspico-utils_1.0+git20130326-3+rpi1_armhf.deb
wget http://archive.raspberrypi.org/debian/pool/main/s/svox/libttspico0_1.0+git20130326-3+rpi1_armhf.deb
sudo apt install -f ./libttspico0_1.0+git20130326-3+rpi1_armhf.deb ./libttspico-utils_1.0+git20130326-3+rpi1_armhf.deb
```

Speak with
```
pico2wave -w temp.wav "Hello. I am a Raspberry Pi." && aplay -D bluealsa temp.wav
```
