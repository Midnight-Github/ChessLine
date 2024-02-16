from os import path
import toml

class __Setting():
    def __init__(self, path):
        self.path = path
        self.pull()

    def pull(self):
        with open(self.path, 'r') as file:
            self.config = toml.loads(file.read())

    def push(self):
        with open(self.path, 'w') as file:
            toml.dump(self.config, file)

#settings.config[<head>][<key>]
settings = __Setting(path.join(path.dirname(__file__) + "\\..\\data\\config.toml"))