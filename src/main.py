from os import path

with open(path.dirname(path.abspath(__file__)) + "/ui/manager.py") as f:
    exec(f.read())
