import sys
import bluetooth
import pickle


def main():
    all_nodes = [
        ("DC:A6:32:55:FC:D8", "ddedfe7e-d33e-11ee-a587-4714a87c8d30"),
        ("DC:A6:32:33:A9:E7", "aff74348-d359-11ee-bb55-672af5cd9386"),
    ]

    connections: dict[tuple[str, str], bluetooth.BluetoothSocket] = {}

    try:
        while True:
            # Set up connections
            for node in all_nodes:
                if not node in connections:
                    service_matches = bluetooth.find_service(
                        uuid=node[1], address=node[0]
                    )

                    if not len(service_matches) == 0:
                        first_match = service_matches[0]
                        port = first_match["port"]
                        name = first_match["name"]
                        host = first_match["host"]

                        print('Connecting to "{}" on {}'.format(name, host))
                        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

                        sock.connect((host, port))
                        sock.settimeout()
                        connections[node] = sock

            for con in connections.values():
                # TODO check if connection has any data
                data = con.recv(1024)
                con.send("rec\n")
                print(pickle.loads(data))
    except KeyboardInterrupt:
        for con in connections.values():
            pass
        #     con.close()


if __name__ == "__main__":
    main()
