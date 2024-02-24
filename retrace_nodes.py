"""

"""

import openai
import requests


def general_prompt():
    usr_msg = """
    [
        {
        'uuid': 'abde123f-1234-5678-abcd-efghijklmnop',
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
        'timestamp': '2024-02-24 17:30:01.123456',
        'connected_time': '2024-02-24 17:30:05.678901',
        'disconnected_time': '2024-02-24 17:31:05.987654'
    },
    {
        'uuid': 'bcfg456h-5678-9012-ijkl-mnopqrstuvwx',
        'metadata': {
            'Customer_Service_Center': 'ahead',
            'Telephones': 'left',

        },
        'node_name': 'Panorama View',
        'timestamp': '2024-02-24 18:45:23.987654',
        'connected_time': '2024-02-24 18:45:28.123456',
        'disconnected_time': '2024-02-24 18:46:28.234567'
    },
    {
        'uuid': 'cdef789i-9012-3456-jklm-nopqrstuvwxyz',
        'metadata': {
            'Customer_Service_Center': 'right',
              'Ground_Transport': 'right'
        },
        'node_name': 'Aero Lounge',
        'timestamp': '2024-02-24 19:30:00.123456',
        'connected_time': '2024-02-24 19:30:05.987654',
        'disconnected_time': '2024-02-24 19:31:06.789012'
    },
    {
        'uuid': 'defg890j-2345-6789-klmn-opqrstuvwxy',
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
        'timestamp': '2024-02-24 20:15:20.987654',
        'connected_time': '2024-02-24 20:15:25.123456',
        'disconnected_time': '2024-02-24 20:16:25.345678'
    },
    {
        'uuid': 'efgh901k-3456-7890-mnop-qrstuvwxyza',
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
        'timestamp': '2024-02-24 21:45:30.123456',
        'connected_time': '2024-02-24 21:45:35.234567',
        'disconnected_time': '2024-02-24 21:46:35.345678'
    },
    {
        'uuid': 'fghi012l-4567-8901-nopq-rstuvwxyzab',
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
        'timestamp': '2024-02-24 22:30:10.987654',
        'connected_time': '2024-02-24 22:30:15.234567',
        'disconnected_time': '2024-02-24 22:31:15.345678'
    },
    {
        'uuid': 'ghij123m-5678-9012-opqr-stuvwxyzabc',
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
        'timestamp': '2024-02-24 23:15:45.987654',
        'connected_time': '2024-02-24 23:15:50.123456',
        'disconnected_time': '2024-02-24 23:16:50.234567'
    },
    {
        'uuid': 'hijk234n-6789-0123-pqrs-tuvwxyzabcd',
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
        'timestamp': '2024-02-24 23:15:45.123754',
        'connected_time': '2024-02-24 23:15:50.483721,
        'disconnected_time': '2024-02-24 23:16:50.503713
    }]

    I'll give you a log that look like this. This is the log of the locations that I passed by. I \
    will ask you questions about some of the services that I passed by. Please let me know the \
    nearest location I can find that place. explain it using the node_name that appeared before \
    and after it. for example, if I ask you where is my nearest bathroom? You can tell me that \
    it's located near my lounge just after starlight lounge.

    Another example: If I ask you restaurant, it's located in horizon view that you passed before \
    starlight lounge and after sunset lounge

    Please don't say 'based on the log provided' or any other thing other than where it is located.\
     Also mention where it is located first then say after and before.
    """
    general_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": usr_msg}]
    )
    return (usr_msg, general_response)


def generate_answer(node_list):

    # response = get_gpt_response(img_path)
    # response_cut = str(response.json()["choices"][0]["message"]["content"])
    # response_dict = response_cut[response_cut.find("{") :]

    # cleaned_dict = {}
    # total_places = response_dict.count(":")
    # for i in range(total_places):
    #     this_key_full = response_dict[: response_dict.find(":")].strip()
    #     this_key = this_key_full[this_key_full.find(" ") :].strip()
    #     response_dict = response_dict[response_dict.find(":") + 1 :]

    #     if i == total_places - 1:
    #         this_value = response_dict[: response_dict.find("}")].strip()
    #     else:
    #         this_value = response_dict[: response_dict.find(",")].strip()

    #     this_key = this_key.replace("_", " ")
    #     this_value = this_value.replace("_", " ")
    #     cleaned_dict[this_key.strip('"')] = this_value.strip('"')

    return answer
