import json


def convert_json(response):
    """
    Convert json response body to python dict
    """
    return json.loads(response.content)
