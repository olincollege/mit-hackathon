"""
Helper functions to generate metadata for a given image.
"""

import base64
import requests
import constants  # contains API key as string assigned to variable api_key


def encode_img(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def generate_metadata(img_path):
    response = get_gpt_response(img_path)
    response_cut = str(response.json()["choices"][0]["message"]["content"])
    response_dict = response_cut[response_cut.find("{") :]

    cleaned_dict = {}
    total_places = response_dict.count(":")
    for i in range(total_places):
        this_key_full = response_dict[: response_dict.find(":")].strip()
        this_key = this_key_full[this_key_full.find(" ") :].strip()
        response_dict = response_dict[response_dict.find(":") + 1 :]

        if i == total_places - 1:
            this_value = response_dict[: response_dict.find("}")].strip()
        else:
            this_value = response_dict[: response_dict.find(",")].strip()

        this_key = this_key.replace("_", " ")
        this_value = this_value.replace("_", " ")
        cleaned_dict[this_key.strip('"')] = this_value.strip('"')

    return cleaned_dict


def get_gpt_response(img_path):
    base64_img = encode_img(img_path)
    prompt = 'Please examine the image and provide the directions to objects present in it, relative to my point of view, in a JSON format. The JSON file should look like `{"restaurant" : "right", "parking" : "ahead", "seating" : "left"}. Include facilities such as restrooms, elevators, information desks, exits, restaurants, and any transportation services like taxi stands or railway stations if visible. Also include any other relevant information regarding facilities. Do not include information about people, the general environment, or decorative elements. Be specific with the names of different locations. If the object is not visible don\'t include it in the JSON. For any signs, give direction direction according to the arrow, if there\'s no arrow present, just say here. Double check each entry in the JSON to make sure it is in the image'

    headers = {"Content-Type": "/json", "Authorization": f"Bearer {constants.API_KEY}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    return response
