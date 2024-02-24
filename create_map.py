import generate_metadata as gm
import map_process as mp


def main():
    img_path = "images/stata.jpeg"
    nodes = mp.generate_nodes(img_path)
    mp.assign_metadata(nodes, "images/img1.jpg", nodes[0]["uuid"])
    mp.create_yaml(nodes, "stata_nodes")


main()
