import sys
import asyncio
import asyncio.streams
import argparse
import json


class CHIPServer:
    def __init__(self, port):
        self.server = None
        self.clients = {}
        self.__port = port

    def _accept_client(self, client_reader, client_writer):
        task = asyncio.Task(self._handle_client(client_reader))
        self.clients[task] = (client_reader)

        def client_done(task):
            del self.clients[task]

        task.add_done_callback(client_done)

    @asyncio.coroutine
    def _handle_client(self, client_reader):
        while True:
            data = (yield from client_reader.readline()).decode("utf-8")
            if not data:
                break
            self.__process_command(data)

    def start(self, loop):
        self.server = loop.run_until_complete(
            asyncio.streams.start_server(self._accept_client,
                                         '127.0.0.1', self.__port,
                                         loop=loop))

    def stop(self, loop):
        """
        Stops the TCP server, i.e. closes the listening socket(s).

        This method runs the loop until the server sockets are closed.
        """
        if self.server is not None:
            self.server.close()
            loop.run_until_complete(self.server.wait_closed())
            self.server = None

    def __process_command(self, data):
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError as error:
            print("ERROR: Could not parse message " + data)
        print("RCV: " + data)


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

