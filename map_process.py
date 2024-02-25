"""
Process a floor plan to place nodes in each important location and associate them with a label,
unique id, and coordinates
"""

import matplotlib.pyplot as plt
import keras_ocr
import uuid
import yaml

import generate_metadata as gm


def generate_nodes(img_path):
    img = keras_ocr.tools.read(img_path)

    pipeline = keras_ocr.pipeline.Pipeline()
    prediction_groups = pipeline.recognize([img])

    myuuid = uuid.uuid4()

    map_nodes = []

    # clean ocr data room_name and getting the center point
    for i in range(len(prediction_groups[0])):
        room = prediction_groups[0][i]
        room_name = prediction_groups[0][i][0]

        if room_name[0:2] == "da":
            room_name = "d4" + room_name[2::]

        x1, y1 = prediction_groups[0][i][1][0]
        x2, y2 = prediction_groups[0][i][1][1]
        x3, y3 = prediction_groups[0][i][1][2]
        x4, y4 = prediction_groups[0][i][1][3]

        xmid = (x1 + x2 + x3 + x4) / 4
        ymid = (y1 + y2 + y3 + y4) / 4
        map_nodes.append(
            {
                "node_name": room_name,
                "uuid": str(uuid.uuid4()),
                "x_coord": str(xmid),
                "y_coord": str(ymid),
                "meta_data": [],
            }
        )
    return map_nodes


def assign_metadata(map_nodes, img_paths_node_dict):
    for img_path, node in img_paths_node_dict.items():
        metadata_dict = gm.generate_metadata(img_path)
        for item in map_nodes:
            if item["node_name"] == node:
                item["meta_data"] = metadata_dict
    return map_nodes


def create_yaml(map_nodes, file_name):
    with open(f"{file_name}.yaml", "w", encoding="utf-8") as yaml_file:
        map_nodes_yaml = yaml.dump(map_nodes, explicit_start=True, default_flow_style=False)
        yaml_file.write(map_nodes_yaml)
