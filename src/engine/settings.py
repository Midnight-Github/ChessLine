from os import path
import json

class __Settings():
    def __init__(self, path):
        self.path = path
        self.pull()

    def pull(self):
        with open(self.path, 'r') as file:
            self.config = json.loads(file.read())

    def push(self):
        with open(self.path, 'w') as file:
            json.dump(self.config, file, indent=4)

settings = __Settings(path.join(path.dirname(__file__) + "\\..\\data\\config.json"))