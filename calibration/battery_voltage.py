#!/usr/bin/python
"""Display raw readings from the MinIMU in a curses terminal interface.

Run this as a script to play back readings stored in a CSV file.
The curses interface defined here is also used in other scripts in this folder.
"""
import csv
from curses import wrapper
import math
import os
import sys
import time
from ina219 import INA219

SHUNT_OHMS = 0.1
MAX_AMPS = 1


ina = INA219(SHUNT_OHMS, MAX_AMPS)
ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

class Extrema(object):
    def __init__(self):
        self.min = 99999
        self.max = -99999

    def update(self, value):
        if value < self.min:
            self.min = value
        if value > self.max:
            self.max = value
        return self.min, value, self.max


class VoltDisplay(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        stdscr.clear()
        stdscr.addstr(0, 0, '            |   min  |   now  |   max ')
        stdscr.addstr(1, 0, 'Current (mA)|')
        stdscr.addstr(2, 0, 'Voltage (V) |')

        self.voltage_extreme = Extrema()
        self.current_extreme = Extrema()

    def update_current(self):
        self.stdscr.addstr(1, 14, '{:6d} | {:6d} | {:6d}'.format(*self.current_extreme.update(ina.current)))
    def update_voltage(self):
        self.stdscr.addstr(2, 14, '{:6d} | {:6d} | {:6d}'.format(*self.voltage_extreme.update(ina.voltage)))


def main(stdscr):
    display = VoltDisplay(stdscr)

    with open(sys.argv[1]) as f:
        cr = csv.DictReader(f)
        for row in cr:
            display.update_current()
            display.update_voltage()
            stdscr.refresh()
            time.sleep(0.1)

    stdscr.getkey()

if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        sys.exit('Usage: curses_imu.py calibration_file.csv')

    try:
        wrapper(main)
    except KeyboardInterrupt:
        print('^C')
