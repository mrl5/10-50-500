#!/usr/bin/env python3

import sys
import RawCodeProvider

filePath = "/home/kuba/projects/IdeaProjects/JInvestor/src/main/java/com/tuxnet/jinvestor/utils/H2.java"
rawCode = RawCodeProvider.getRawCode(filePath)
print(rawCode)
print(len(rawCode))
