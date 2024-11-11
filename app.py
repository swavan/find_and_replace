import argparse
from dataclasses import dataclass, field
import os
from pathlib import Path
from fileinput import FileInput
from re import compile, IGNORECASE, escape

@dataclass(frozen=True)
class FindReplaceConfig:
    root: str
    find: str
    replace: str
    ignore_file_types: list[str] = field(default_factory=[])

def __main__(config: FindReplaceConfig):
    push = print
    for root, dirs, files in os.walk(config.root):
            for file in files:
                full_path = os.path.join(root, file)
                with FileInput(full_path, inplace=True) as f:
                    for line in f:
                        if config.find.lower() in line.lower():
                            expression = compile(escape(config.find), IGNORECASE)
                            push(expression.sub(config.replace, line), end='')
                        else:
                            push(line, end='')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="find_and_replace")
    parser.add_argument('--root_path', type=Path, help='Root directory to start reading files from') 
    parser.add_argument('--find', type=str, help='What do you like to find') 
    parser.add_argument('--replace', type=str, help='text replace the find content')
    parser.add_argument('--ignore-types', type=list[str], help='ignore file types to be replaced', default=[])
    args = parser.parse_args()
    __main__(FindReplaceConfig(
        root=args.root_path,
        find=args.find,
        replace=args.replace,
        ignore_file_types= args.ignore_types))
