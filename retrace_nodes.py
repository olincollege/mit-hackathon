"""
Helper functions to retrace steps and answer a question
"""

import openai
import requests
import constants


def general_prompt(node_list, question):
    usr_msg = """
    [
        {
        'metadata': {
            'Customer_Service_Center': 'left',
            'Telephones': 'right',
               'Gate_C20': 'left',
            'Gates_C18_C18A': 'right',
            'Terminals': 'ahead',
            'Concourses': 'left',
            'Baggage_Claim': 'ahead',
            'Ground_Transport': 'right'
        },
        'node_name': 'Sky Lounge',
        'connected_time': '2024-02-24 17:30:05.678901',
        'disconnected_time': '2024-02-24 17:31:05.987654'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'ahead',
            'Telephones': 'left',

        },
        'node_name': 'Panorama View',
        'connected_time': '2024-02-24 18:45:28.123456',
        'disconnected_time': '2024-02-24 18:46:28.234567'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'right',
              'Ground_Transport': 'right'
        },
        'node_name': 'Aero Lounge',
        'connected_time': '2024-02-24 19:30:05.987654',
        'disconnected_time': '2024-02-24 19:31:06.789012'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'ahead',
            'Telephones': 'right',
            'Restrooms': 'right',
            'Restaurant': 'left',


            'Concourses': 'ahead',
            'Baggage_Claim': 'right',
            'Ground_Transport': 'left'
        },
        'node_name': 'Cloud Nine',
        'connected_time': '2024-02-24 20:15:25.123456',
        'disconnected_time': '2024-02-24 20:16:25.345678'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'right',
                     'Restaurant': 'left',
            'Gate_C20': 'ahead',
            'Gates_C18_C18A': 'right',
            'Terminals': 'left',
            'Concourses': 'right',
            'Baggage_Claim': 'ahead',
            'Ground_Transport': 'left'
        },
        'node_name': 'Sunset Lounge',
        'connected_time': '2024-02-24 21:45:35.234567',
        'disconnected_time': '2024-02-24 21:46:35.345678'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'left',
            'Telephones': 'ahead',
            'Restrooms': 'right',
            'Restaurant': 'ahead',
            'Gate_C20': 'right',
            'Gates_C18_C18A': 'left',

            'Ground_Transport': 'ahead'
        },
        'node_name': 'Horizon View',
        'connected_time': '2024-02-24 22:30:15.234567',
        'disconnected_time': '2024-02-24 22:31:15.345678'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'right',
            'Gate_C20': 'left',
            'Gates_C18_C18A': 'right',
            'Terminals': 'ahead',
            'Concourses': 'left',
            'Baggage_Claim': 'ahead',
            'Ground_Transport': 'right'
        },
        'node_name': 'Starlight Lounge',
        'connected_time': '2024-02-24 23:15:50.123456',
        'disconnected_time': '2024-02-24 23:16:50.234567'
    },
    {
        'metadata': {
            'Customer_Service_Center': 'ahead',
            'Telephones': 'left',
            'Restrooms': 'left',
         ]
            'Concourses': 'ahead',
            'Baggage_Claim': 'right',
            'Ground_Transport': 'right'
        },
        'node_name': My Lounge',
        'connected_time': '2024-02-24 23:15:50.483721,
        'disconnected_time': '2024-02-24 23:16:50.503713
    }]

    I'll give you a log that look like this. This is the log of the locations that I passed by. I \
    will ask you questions about some of the services that I passed by, which are written in 'node_name'. \
    Please let me know the nearest location I can find that place. Explain it using the node_name that appeared before \
    and after it. for example, if I ask you where is my nearest bathroom? You can tell me that \
    it's located near my lounge just after starlight lounge.

    Another example: If I ask you restaurant, it's located in horizon view that you passed before \
    starlight lounge and after sunset lounge

    Please don't say 'based on the log provided' or any other thing other than where it is located.\
    Also mention where it is located first then say after and before.

    This is just a sample log for formatting, so do not include any information about this in a \
    response. Also, start by looking at the entries at the bottom of the list and check upwards \
    from there.
    """

    msg = f"""
    {node_list}

    Here is the log of locations that I passed by. Do not use any other logs to answer my question. \
    Ignore all other log information.

    My question is: {question}. Please don't say 'based on the log provided' or any other thing \
    other than where it is located. Start by searching the log from the end.
    """
    openai.api_key = constants.API_KEY
    general_response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": usr_msg},
            {"role": "assistant", "content": "I will follow this method."},
            {"role": "user", "content": msg},
        ],
    )
    return general_response


def get_metadata(node_list, node_uuid):
    metadata = {}
    for object in node_list:
        if object["uuid"] == node_uuid:
            metadata = object["metadata"]

    if metadata == []:
        return "There are no important features detected here."

    if len(metadata) == 1:
        return f"There is a {metadata.keys[0]} {metadata.values[0]}"

    answer = "There is a "
    for key, value in metadata:
        midword = ""
        if value in ["left", "right"]:
            midword = " to the"
        answer = answer + f"{key} {midword} {value}, "
    return answer


def generate_answer(node_list, question):
    answer = general_prompt(node_list, question)
    response = answer["choices"][0]["message"]["content"]

    return response
