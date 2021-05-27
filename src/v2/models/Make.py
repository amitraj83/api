import json

class Make:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
