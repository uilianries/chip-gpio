#!/usr/bin/python3

from enum import Enum
from enum import IntEnum
import os
import sys
import argparse

class Mode(Enum):
    output = 'out'
    input = 'in'

class Level(IntEnum):
    low = 0
    high = 1

class Gpio(object):

    __PIN_BASE = 408
    __CLASS_DIR = '/sys/class/gpio'
    __PIN_MAX = 8

    def run(self, args):
        self.__pin_validation(args.pin)

        if args.command == 'enable':
            self.__enable(args.pin)
        elif args.command == 'disable':
            self.__disable(args.pin)
        elif args.command == 'mode':
            mode = self.__str_to_mode(args.mode)
            self.__mode_validation(mode)
            self.__mode(args.pin, mode)
        elif args.command == 'write':
            level = self.__str_to_level(args.level)
            self.__level_validation(level)
            self.__write(args.pin, level)
        elif args.command == 'read':
            result = self.__read(args.pin)
            sys.stdout.write(result)
            sys.stdout.flush()
        else:
            raise AssertionError('Invalid command')

    def __mode_validation(self, mode: Mode):
        if mode is None:
            raise AssertionError('Option mode is mandatory')
        if mode is not Mode.output and mode is not Mode.input:
            raise AssertionError('Option mode is invalid')

    def __pin_validation(self, pin: int):
        if pin is None:
            raise AssertionError('Option pin must is mandatory')
        if pin < 0 or pin > Gpio.__PIN_MAX:
            raise AssertionError('Option pin must be 0..8')

    def __level_validation(self, level: Level):
        if level is None:
            raise AssertionError('Option level must is mandatory')
        if level is not Level.high and level is not Level.low:
            raise AssertionError('Level option is invalid')

    def __str_to_level(self, str_level: str):
        level_dict = {'low': Level.low, 'high': Level.high}
        return level_dict[str_level]

    def __str_to_mode(self, str_mode: str):
        mode_dict = {'input': Mode.input, 'output': Mode.output}
        return mode_dict[str_mode]

    def __to_gpio(self, pin: int):
        return str(Gpio.__PIN_BASE + pin)

    def __enable(self, pin: int):
        export_path = os.path.join(Gpio.__CLASS_DIR, 'export')
        fd = open(export_path, 'w')
        fd.write(self.__to_gpio(pin))

    def __disable(self, pin: int):
        unexport_path = os.path.join(Gpio.__CLASS_DIR, 'unexport')
        fd = open(unexport_path, 'w')
        fd.write(self.__to_gpio(pin))

    def __mode(self, pin: int, mode: Mode):
        gpio_dir = os.path.join(Gpio.__CLASS_DIR, 'gpio' + self.__to_gpio(pin))
        if not os.path.isdir(gpio_dir):
            raise IOError("Pin {0} is not enabled".format(str(self.__to_gpio(pin))))
        fd = open(os.path.join(gpio_dir, 'direction'), 'w')
        fd.write(str(mode.value))

    def __read(self, pin: int):
        gpio_dir = os.path.join(Gpio.__CLASS_DIR, 'gpio' + self.__to_gpio(pin))
        if not os.path.isdir(gpio_dir):
            raise IOError("Pin {0} is not enabled".format(str(pin)))
        fd = open(os.path.join(gpio_dir, 'value'), 'r')
        return fd.read()

    def __write(self, pin: int, level: Level):
        gpio_dir = os.path.join(Gpio.__CLASS_DIR, 'gpio' + self.__to_gpio(pin))
        if not os.path.isdir(gpio_dir):
            raise IOError("Pin {0} is not enabled".format(str(pin)))
        fd = open(os.path.join(gpio_dir, 'value'), 'w')
        return fd.write(str(level.value))

def main():
    parser = argparse.ArgumentParser(description = 'GPIO Management.')
    parser.add_argument('command', type = str, help = 'Command to be executed: [enable|disable|mode|read|write]')
    parser.add_argument('pin', type = int, help = 'GPIO Pin: [0..8]')
    parser.add_argument('--mode', type = str, help = 'GPIO direction: [input|output]')
    parser.add_argument('--level', type = str, help = 'GPIO level: [high|low]')
    arguments = parser.parse_args()

    gpio = Gpio()
    gpio.run(arguments)

if __name__ == "__main__":
    main()
