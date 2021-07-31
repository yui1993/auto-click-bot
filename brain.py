import json
from objectify import Objectify as obj

class Brain():
    def __init__(self, file="brain/brain.json"):
        self._file = file
        self.brain = None
    
    def load(self, file=None):
        if file:
            self._file = file
        with open(self._file, "r") as f:
            self.brain = obj(json.loads(f.read()))
    
    def save(self, file=None):
        if file:
            self._file = file
        with open(self._file, "w") as f:
            f.write(json.dumps(self.brain.toDict()))
    