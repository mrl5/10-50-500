#!/usr/bin/env python3

import sys
import RawCodeProvider

filePath = sys.argv[1] #"/home/kuba/projects/IdeaProjects/JInvestor/src/main/java/com/tuxnet/jinvestor/utils/H2.java"
rawCode = RawCodeProvider.getRawCode(filePath)
print("SLOC:", len(rawCode))
