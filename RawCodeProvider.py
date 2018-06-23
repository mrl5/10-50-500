#!/usr/bin/env python3

import re


def getRawCode(filePath):
    with open(filePath, "r") as f:
        rawCode = []
        multiLineComment = False

        for line in f:
            line = re.sub(r'^\s+', '', line).rstrip()
            line = re.sub(r'^\/\*.*\*\/', '', line).rstrip()

            if line != '':
                if (re.match(r'^\/(\*)+', line)):
                    multiLineComment = True
                    continue
                elif (re.match(r'(\*)+\/', line)):
                    multiLineComment = False
                    continue
                elif (multiLineComment == False):
                    rawCode.append(line)
    return rawCode
