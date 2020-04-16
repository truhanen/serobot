#!/usr/bin/python

import time
import smbus
import logging

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================


# Module-level logger
logger = logging.getLogger(__name__)


class PCA:
    # Registers/etc.
    _SUBADR1            = 0x02
    _SUBADR2            = 0x03
    _SUBADR3            = 0x04
    _MODE1              = 0x00
    _PRESCALE           = 0xFE
    _LED0_ON_L          = 0x06
    _LED0_ON_H          = 0x07
    _LED0_OFF_L         = 0x08
    _LED0_OFF_H         = 0x09
    _ALLLED_ON_L        = 0xFA
    _ALLLED_ON_H        = 0xFB
    _ALLLED_OFF_L       = 0xFC
    _ALLLED_OFF_H       = 0xFD

    mode_bit_sleep = 4
    mode_bit_restart = 7

    channel_pan = 0
    channel_tilt = 1

    _pwm_freq = 50

    def __init__(self, address=0x40):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.reset()
        self._set_pwm_freq()

    def write(self, reg, value):
        """Write an 8-bit value to the specified register/address"""
        self.bus.write_byte_data(self.address, reg, value)
        logger.debug('I2C: Write {:#b} to register {:#b}'.format(value, reg))

    def read(self, reg):
        """Read an unsigned byte from the I2C device"""
        result = self.bus.read_byte_data(self.address, reg)
        logger.debug('I2C: Device {:#b} returned {:#b} from reg {:#b}'.format(self.address, result & 0xFF, reg))
        return result

    def set_mode_value(self, value):
        self.write(self._MODE1, value)

    def get_mode_value(self):
        self.read(self._MODE1)

    def set_mode_bit(self, mode_bit, on=True):
        bin_value = 1 << mode_bit
        old_mode = self.get_mode_value() or 0b00000000
        if on:
            self.set_mode_value(old_mode | bin_value)
        else:
            complement_bin_value = bin_value ^ 0b11111111
            self.set_mode_value(old_mode & complement_bin_value)

    def reset(self):
        logger.debug('Resetting PCA9685')
        self.set_mode_value(0b00000000)

    def sleep(self, sleep=True):
        logger.debug('Setting sleep {}'.format(sleep))
        self.set_mode_bit(self.mode_bit_sleep, sleep)
        if not sleep:
            # Wait for oscillator to stabilize
            time.sleep(0.0051)
            # Restart PWM channels by setting the RESTART bit
            self.set_mode_bit(self.mode_bit_restart, True)

    def _set_pwm_freq(self):
        """Set the PWM frequency"""
        oscillator_freq = 25e6
        prescale_value = oscillator_freq / 4096 / self._pwm_freq
        prescale_value = int(round(prescale_value)) - 1
        logger.debug('Setting PWM frequency to {} Hz'.format(self._pwm_freq))

        # Set SLEEP bit on for setting the PRE_SCALE register
        self.sleep()
        # Set PRE_SCALE
        self.write(self._PRESCALE, prescale_value)
        # Return from sleep
        self.sleep(False)

    def set_pwm(self, channel, off):
        """Sets a single PWM channel"""
        self.write(self._LED0_ON_L + 4 * channel, 0)
        self.write(self._LED0_ON_H + 4 * channel, 0)
        self.write(self._LED0_OFF_L + 4 * channel, off & 0b11111111)
        self.write(self._LED0_OFF_H + 4 * channel, off >> 8)

    def set_servo_pulse(self, channel, pulse):
        """Sets the servo pulse

        Arguments
        =========
        channel: PCA.channel_pan | PCA.channel_tilt
            Pan/tilt channel
        pulse: int
            Servo duty cycle in milliseconds. 1500 is center.
        """
        logger.debug('Setting servo {} pulse {}'.format(channel, pulse))
        period_us = 1 / self._pwm_freq * 1000000
        pulse = int(pulse * 4096 / period_us)
        self.set_pwm(channel, pulse)

if __name__=='__main__':
    center_value = 1500
    min_pan = 900
    max_pan = 2100
    min_tilt = 600
    max_tilt = 2300

    p = PCA(debug=True)

    if 1:
        import random
        for i in range(10):
            pan = random.randint(min_pan, max_pan)
            tilt = random.randint(min_tilt, max_tilt)
            p.set_servo_pulse(0, pan)
            p.set_servo_pulse(1, tilt)
            time.sleep(1)
        p.set_servo_pulse(0, center_value)
        p.set_servo_pulse(1, center_value)

    if 0:
        for pulse in list(range(min_pan, max_pan + 1, 50)) + [center_value]:
            p.set_servo_pulse(0, pulse)
            time.sleep(.5)

        for pulse in list(range(min_tilt, max_tilt + 1, 50)) + [center_value]:
            p.set_servo_pulse(1, pulse)
            time.sleep(.5)

    if 0:
        while True:
            for i in range(500, 2500, 10):
                p.set_servo_pulse(0, i)
                time.sleep(.02)
            for i in range(2500, 500, -10):
                p.set_servo_pulse(0, i)
                time.sleep(.02)

    print('Finished')
