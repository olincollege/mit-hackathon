#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $
"""

import bluetooth
import pickle
import time
import datetime
import yaml
import argparse
from pathlib import Path
from yaml import Loader

NODE_DATA_PATH = Path(__file__).parent / "map_nodes.yaml"


def establish_ble(server_sock, port):
    print("Waiting for connection on RFCOMM channel", port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    return client_sock


def parse_yaml(idx: int):
    with open(NODE_DATA_PATH, "r") as file:
        data = yaml.safe_load(file)
    del data[idx]["x_coord"]
    del data[idx]["y_coord"]
    return data[idx]


def main(idx: int):
    node_data = parse_yaml(idx)
    uuid = node_data["uuid"]
    print(f"Device UUID: {uuid}")

    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    bluetooth.advertise_service(
        server_sock,
        "localization_transmitter",
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
        # protocols=[bluetooth.OBEX_UUID]
    )

    client_sock = establish_ble(server_sock, port)
    while True:
        try:
            client_sock.send(pickle.dumps(node_data, -1))
            data = client_sock.recv(1024)
            print(f"{datetime.datetime.now().__str__()}\t{data}")
        except bluetooth.btcommon.BluetoothError:
            client_sock = establish_ble(server_sock, port)

        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Setup Raspberry Pi Transmitters",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-idx",
        type=int,
        help="Index in `map_nodes.yaml` to set this BLE Device with",
        default=0,
    )
    args = parser.parse_args()
    main(args.idx)
