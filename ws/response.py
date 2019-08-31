import json


class Response:
    """
    Response class
    """

    def __init__(self, action=None, message=None):
        self.action = action
        self.message = message

    def __str__(self):
        return json.dumps({"action": self.action, "message": self.message})
