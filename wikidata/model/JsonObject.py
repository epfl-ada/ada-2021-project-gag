import json


class JsonObject:
    """
    Class that represents a JSON object
    Attributes:
      - params: dict[str, str]
            JSON object in one of its string forms
    """

    def __init__(self, params: dict):
        self.json = params

    def prettyFormat(self):
        """Generates a pretty printable string representation of the JSON object"""
        return json.dumps(self.json, indent = 4, sort_keys = True)

    def prettyPrint(self):
        """Pretty prints the JSON object"""
        print(self.prettyFormat())
