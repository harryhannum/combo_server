import argparse
import socket
import threading
import struct
import json
from source_locator import *


def get_version_source(sources_json, project_name, version):
    source_locator = SourceLocator(sources_json)
    return source_locator.get_source(project_name, version)


def handle_client_connection(client_socket):
    ack = struct.pack('>i', 0xF00BA4)
    req_length = client_socket.recv(4)
    print(req_length)
    length = struct.unpack('>i', req_length)[0]

    client_socket.send(ack)
    encoded = client_socket.recv(length)
    decoded = tuple(encoded.decode().split(';'))
    # client_socket.send(ack)

    result = get_version_source('sources.json', *decoded)
    dump = json.dumps(vars(result)).encode()

    client_socket.send(dump)
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
