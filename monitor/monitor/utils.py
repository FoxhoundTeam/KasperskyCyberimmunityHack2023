import json

from .exceptions import InvalidJSONException


def parse_json(data: str):
    try:
        return json.loads(data)
    except Exception as e:
        raise InvalidJSONException from e
