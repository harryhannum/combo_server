import argparse
import socket
import threading
import struct
from server_source_locator import *


MAX_REQUEST_LENGTH = 256
ACK_MSG = struct.pack('>i', 0xF00BA4)
NACK_MSG = struct.pack('>i', 0xDEC11E)
SOURCES_JSON = 'sources.json'

source_locator = ServerSourceLocator(SOURCES_JSON)


def handle_client_connection(client_socket):
    try:
        request_length = client_socket.recv(4)

        unpacked_length = struct.unpack('>i', request_length)[0]
        assert unpacked_length <= MAX_REQUEST_LENGTH,\
            'Unsupported request length (received {}, max is {})'.format(unpacked_length, MAX_REQUEST_LENGTH)
        client_socket.send(ACK_MSG)

        request = client_socket.recv(unpacked_length)
        assert len(request) == unpacked_length,\
            'Received {} bytes of request instead of {}'.format(len(request), unpacked_length)

        request_tuple = tuple(request.decode().split(';'))
        assert len(request_tuple) == 2, 'Expected a request with project name and version number'

        project_name, version = request_tuple
        VersionNumber(version)  # Make sure version is valid

        source = source_locator.get_source(project_name, version)
        client_socket.send(source.as_dict().encode())

    except BaseException as e:
        client_socket.send(NACK_MSG)
        print('Failed to handle request from', client_socket)
        print(e, '\n')

    client_socket.close()


def main():
    parser = argparse.ArgumentParser(description='Combo Server Arguments')
    parser.add_argument('port', help='TCP Port', type=int)
    parser.add_argument('sources_json', help='A sources json')
    args = parser.parse_args()

    address = ('0.0.0.0', args.port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(5)  # max backlog of connections

    print('Listening on {}:{}'.format(*address))

    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(*address))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()


if __name__ == '__main__':
    main()
