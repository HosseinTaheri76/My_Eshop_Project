import json


def get_message(path):
    with open('message.json', 'r', encoding='utf-8') as f:
        dict_data = json.loads(f.read())
    keys = path.split('/')
    message = dict_data[keys[0]]
    for key in keys[1:]:
        message = message[key]
    return message
