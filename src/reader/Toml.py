from os import path
import toml

class Toml():
    def __init__(self, rel_path: str) -> None:
        self.path = path.dirname(__file__) + rel_path
        self.pull()

    def pull(self) -> None:
        with open(self.path, 'r') as file:
            self.config = toml.loads(file.read())

    def push(self) -> None:
        with open(self.path, 'w') as file:
            toml.dump(self.config, file)

#configurator.config[<head>][<key>]
configurator = Toml("\\..\\data\\config.toml")