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

test_data = {
    "uuid": "ddedfe7e-d33e-11ee-a587-4714a87c8d30",
    "metadata": "There is a bathroom nearby",
    "node_name": "Vertigo Room",
    "timestamp": str(datetime.datetime.now())
}

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = test_data["uuid"]


bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

def establish_ble():
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    return client_sock, client_info
print("Waiting for connection on RFCOMM channel", port)

def main():
    client_sock, client_info = establish_ble()
    while True:
        test_data["time"] = str(datetime.datetime.now())
        try:
            client_sock.send(pickle.dumps(test_data, -1))
            data = client_sock.recv(1024)
            print(data)
        except bluetooth.btcommon.BluetoothError:
            client_sock, client_info = establish_ble()

        time.sleep(1)

if __name__ == "__main__":
    main()