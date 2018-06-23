#!/usr/bin/env python3

import re
import sys


def get_raw_code(file_path):
    with open(file_path, "r") as f:
        raw_code = []
        multi_line_comment = False

        for line in f:
            # remove spaces from the beggining of the line
            line = re.sub(r'^\s+', '', line).rstrip()
            # remove '/* comments */'
            line = re.sub(r'^\/\*.*\*\/', '', line).rstrip()
            # remove '//comments'
            line = re.sub(r'^\/\/.*', '', line).rstrip()

            # ignore empty lines
            if line != '':
                # skip /** multi-line comments
                if re.match(r'^\/(\*)+', line):
                    multi_line_comment = True
                    continue

                # check if multi-line comment was closed
                elif re.match(r'(\*)+\/', line):
                    multi_line_comment = False
                    continue

                # add line if it's not multi-line comment
                if not multi_line_comment:
                    raw_code.append(line)
    return raw_code


if __name__ == "__main__":
    path = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
    for raw_line in get_raw_code(path):
        print(raw_line)
