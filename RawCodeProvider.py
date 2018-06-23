#!/usr/bin/env python3

import re
import sys


def getRawCode(filePath):
    with open(filePath, "r") as f:
        rawCode = []
        multiLineComment = False

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
                if (re.match(r'^\/(\*)+', line)):
                    multiLineComment = True
                    continue

                # check if multi-line comment was closed
                elif (re.match(r'(\*)+\/', line)):
                    multiLineComment = False
                    continue

                # add line if it's not multi-line comment
                elif (multiLineComment == False):
                    rawCode.append(line)
    return rawCode


if __name__ == "__main__":
    filePath = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
    for line in getRawCode(filePath):
        print(line)
