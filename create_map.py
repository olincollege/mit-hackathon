import generate_metadata as gm
import map_process as mp
import retrace_nodes as rn

node_list = """
[
    {
        'metadata': {
            'Restrooms': 'right',
            'Restaurant': 'ahead',
            'Gate_C20': 'left',
            'Terminals': 'left',
            'Concourses': 'left',
            'Baggage_Claim': 'left'
        },
        'node_name': 'gate1',
        'connected_time': '2024-02-25 08:00:10',
        'disconnected_time': '2024-02-25 08:01:10'
    },
    {
        'metadata': {
            'Telephones': 'left',
            'Restrooms': 'right',
            'Gate_C20': 'left',
            'Terminals': 'right',
            'Ground_Transport': 'ahead'
        },
        'node_name': 'exit',
        'connected_time': '2024-02-25 08:15:20',
        'disconnected_time': '2024-02-25 08:16:20'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'right',
            'Telephones': 'right',
            'Restaurant': 'left',
            'Gate_C20': 'left',
            'Concourses': 'right',
            'Baggage_Claim': 'right',
            'Ground_Transport': 'right'
        },
        'node_name': 'gate43',
        'connected_time': '2024-02-25 08:30:30',
        'disconnected_time': '2024-02-25 08:31:30'
    },
    {
        'metadata': {
            'Telephones': 'ahead',
            'Restrooms': 'right',
            'Restaurant': 'ahead',
            'Gate_C20': 'right',
            'Gates_C18_C18A': 'left',
            'Ground_Transport': 'left'
        },
        'node_name': 'gate27',
        'connected_time': '2024-02-25 09:00:45',
        'disconnected_time': '2024-02-25 09:01:45'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'ahead',
            'Restrooms': 'left',
            'Gate_C20': 'ahead',
            'Terminals': 'left',
            'Concourses': 'right',
            'Ground_Transport': 'right'
        },
        'node_name': 'exit',
        'connected_time': '2024-02-25 09:30:15',
        'disconnected_time': '2024-02-25 09:31:15'
    }
]
"""


def main():
    # img_path = "images/stata.jpeg"
    # nodes = mp.generate_nodes(img_path)
    # mp.assign_metadata(nodes, "images/img1.jpg", nodes[0]["uuid"])
    # mp.create_yaml(nodes, "stata_nodes")

    answer = rn.general_prompt(node_list, "Where is the bathroom")
    response = answer["choices"][0]["message"]["content"]


main()
