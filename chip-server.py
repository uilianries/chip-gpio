#!/usr/bin/python3

import sys
import asyncio
import asyncio.streams
import argparse
import json
import subprocess
import logging

logging.basicConfig(filename='chip-server.log',level=logging.DEBUG, format='%(asctime)s|%(name)s|%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class CHIPServer:

    __CHIP_GPIO = 'chip-gpio.py'

    def __init__(self, port):
        self.server = None
        self.clients = {}
        self.port = port
        self.logger = logging.getLogger('chip-server')

    def _accept_client(self, client_reader, client_writer):
        task = asyncio.Task(self._handle_client(client_reader, client_writer))
        self.clients[task] = (client_reader)

        def client_done(task):
            del self.clients[task]

        task.add_done_callback(client_done)

    @asyncio.coroutine
    def _handle_client(self, client_reader, client_writer):
        self.logger.info('New client was accepted')
        while True:
            data = (yield from client_reader.readline()).decode("utf-8")
            if not data:
                break
            try:
                self.logger.info('Received data: ' + data)
            except:
                selg.logger.error("Could not log received message")
            self.__process_command(data, client_writer)

    def start(self, loop):
        self.logger.info('Starting CHIP server')
        self.server = loop.run_until_complete(
            asyncio.streams.start_server(self._accept_client,
                                         '127.0.0.1', self.port,
                                         loop=loop))

    def stop(self, loop):
        self.logger.info('Stoping CHIP server')
        if self.server is not None:
            self.server.close()
            loop.run_until_complete(self.server.wait_closed())
            self.server = None

    def __process_command(self, data, client_writer):
        try:
            json_data = json.loads(data)
        except:
            self.logger.error("Could not parse message")
            return

        command = None
        pin = None
        try:
            json_dict = json_data[0]
            command = json_dict['command']
            pin = json_dict['pin']
            data = [{'command': 'enable', 'result': False}]

            if command == 'enable':
                data[0]['result'] = self.__enable(pin)
            elif command == 'disable':
                data[0]['result'] = self.__disable(pin)
            elif command == 'mode':
                data[0]['result'] = self.__mode(pin, json_dict['mode'])
            elif command == 'write':
                data[0]['result'] = self.__write(pin, json_dict['level'])
            elif command == 'read':
                data[0]['result'] = True
                data[0]['answer'] = self.__read(pin)
            else:
                self.logger.error('Invalid command: ' + command)

            client_writer.write("{!r}".format(data).rstrip('\r\n').encode('utf-8'))
        except:
            self.logger.error("Could not parse JSON data")

    def __enable(self, pin: int):
        result = None
        try:
            result = subprocess.call([CHIPServer.__CHIP_GPIO, 'enable', str(pin)])
        except FileNotFoundError as error:
            self.logger.error("Chip gpio is not installed")
        if result is not 0:
            self.logger.error("Could not enable pin " + str(pin))
            return False
        return True

    def __disable(self, pin: int):
        result = None
        try:
            result = subprocess.call([CHIPServer.__CHIP_GPIO, 'disable', str(pin)])
        except FileNotFoundError as error:
            self.logger.error("Chip gpio is not installed")
        if result is not 0:
            self.logger.error("Could not disable pin " + str(pin))
            return False
        return True

    def __mode(self, pin: int,  mode: str):
        result = None
        try:
            result = subprocess.call([CHIPServer.__CHIP_GPIO, 'mode', str(pin), '--mode={}'.format(mode)])
        except FileNotFoundError as error:
            self.logger.error("Chip gpio is not installed")
        if result is not 0:
            self.logger.error("Could not mode pin " + str(pin))
            return False
        return True

    def __write(self, pin: int, level: str):
        result = None
        try:
            result = subprocess.call([CHIPServer.__CHIP_GPIO, 'write', str(pin), '--level={}'.format(level)])
        except FileNotFoundError as error:
            self.logger.error("Chip gpio is not installed")
        if result is not 0:
            self.logger.error("Could not write on pin " + str(pin))
            return False
        return True

    def __read(self, pin: int):
        try:
            proc = subprocess.Popen([CHIPServer.__CHIP_GPIO, 'read', str(pin)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if proc.returncode is not 0:
                self.logger.error("Could not read on pin " + str(pin))
            self.logger.info('Read level {0} at GPIO {1}'.format(out, str(pin)))
            return out
        except FileNotFoundError as error:
            self.logger.error("Chip gpio is not installed")

def main():
    parser = argparse.ArgumentParser(description = 'GPIO Server.')
    parser.add_argument('port', type = int, help = 'Server port to listen')
    arguments = parser.parse_args()

    loop = asyncio.get_event_loop()

    server = CHIPServer(arguments.port)
    server.start(loop)

    try:
        loop.run_forever()
    finally:
        server.stop(loop)
        loop.close()


if __name__ == '__main__':
    main()

