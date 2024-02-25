import datetime
import sys
import bluetooth
import pickle
import bluetooth._bluetooth as bluez
import subprocess
from gtts import gTTS
from io import BytesIO
from io import BytesIO
from pygame import mixer
from pydub import AudioSegment
import time
from pynput.keyboard import Key, Listener


def tts_play(text):
    tts = gTTS(text)
    audio_bytes_io = BytesIO()
    tts.write_to_fp(audio_bytes_io)
    audio_bytes_io.seek(0)
    audio = AudioSegment.from_file(audio_bytes_io, format="mp3")
    audio_duration = len(audio) / 1000.0
    audio_bytes_io.seek(0)
    mixer.music.load(audio_bytes_io, "mp3")
    mixer.music.play()
    time.sleep(audio_duration)


def get_rssi(device_address):
    result = subprocess.run(
        ["hcitool", "rssi", device_address], capture_output=True, text=True
    )
    output = result.stdout.strip()
    # TODO error handling for not connected
    rssi = int(output.split(": ")[1])
    return rssi

metadata_pressed = False
question_pressed = False
def main():
    global metadata_pressed, question_pressed
    metadata_pressed = False
    question_pressed = False
    def show(key):
        global metadata_pressed, question_pressed
        if key == Key.right:
            question_pressed = True
        if key == Key.left:
            metadata_pressed = True

        if key == Key.delete:
            return False

    listener = Listener(on_press=show)
    listener.start()
    mixer.init()
    all_nodes = [
        ("DC:A6:32:55:FC:D8", "62f1730b-9f3d-4e20-8255-3b97d19bf866"),
        # ("DC:A6:32:33:A9:E7", "3521e14d-e48d-46d2-aab9-89a50c1e4272"),
    ]

    connections: dict[tuple[str, str], bluetooth.BluetoothSocket] = {}
    connections_data: dict[tuple[str, str], dict] = {}

    data_history = []

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
                        sock.settimeout(4)
                        connections[node] = sock

            # Read Data in the connections
            for node, con in connections.items():
                rssi = get_rssi(node[0])
                if rssi > -5:
                    data = con.recv(1024)
                    con.send("rec\n")
                    data_dict = pickle.loads(data)
                    data_dict["signal_strength"] = rssi
                    print(data_dict)
                    if not node in connections_data:
                        # Add data on first connection
                        print(f"Added first connect data for {node[0]}")
                        data_dict["connected_time"] = datetime.datetime.now()
                        connections_data[node] = data_dict
                        tts_play(f"Approaching room {data_dict['node_name']}")
                else:
                    # End the socket connection on out of range
                    if node in connections_data:
                        print("Connection is out of range")
                        connections_data[node][
                            "disconnected_time"
                        ] = datetime.datetime.now()
                        data_history.append(connections_data.pop(node))
                        tts_play(f"Leaving room {data_dict['node_name']}")

            # Check for any user inputs
            if question_pressed:
                print("Question Pressed")
                question_pressed = False
            if metadata_pressed:
                print("Meta Pressed")
                metadata_pressed = False

    except KeyboardInterrupt:
        for con in connections.values():
            con.close()


if __name__ == "__main__":
    main()
