import os
from typing import Sequence
import re

def getLine(path):
    with open(path, 'r', encoding='utf-8') as f:
        yield from f

def totalLines(func):
    lines = dict.fromkeys(range(0, 128), 0)
    def wrapper(*args, **kwargs):
        dir_total_lines, indent = func(*args, **kwargs)
        lines[indent] += dir_total_lines
        total_lines = 0
        for k, v in lines.items():
            if indent < k:
                total_lines += v

        print('    '*indent + "Total Lines:", total_lines + dir_total_lines)

    return wrapper

def endsWith(string:str, seq:Sequence) -> bool:
    for i in seq:
        if string.endswith(i):
            return True
    return False

@totalLines
def countLines(path:str, extensions:Sequence, black_list:Sequence=tuple(), indent:int=1) -> tuple[int, int]:
    total_lines = 0
    if indent == 1: 
        search = re.search(r'[\\/]?([^\\^/]+)$', path)
        if search is None:
            raise ValueError("Cannot find dir name in specified path")
        
        print('-'*10, search.group(1), '-'*10)

    for i in os.listdir(path):
        curr_path = path + "/" + i
        if i in black_list:
            continue

        if os.path.isdir(curr_path):
            print('    '*indent + '-'*10, i, '-'*10)
            countLines(curr_path, extensions=extensions, black_list=black_list, indent=indent + 1)

        if endsWith(i, extensions):
            lines = 0
            for _ in getLine(curr_path):
                lines += 1
            print('    '*indent + f"{i}: {lines}")
            total_lines += lines
        
    return (total_lines, indent)

countLines("src", (".py", ".toml"), ("__pycache__", "__init__.py"))
