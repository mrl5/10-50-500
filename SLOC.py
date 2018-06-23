#!/usr/bin/env python3

import sys
import RawCodeProvider

filePath = sys.argv[1]
rawCode = RawCodeProvider.getRawCode(filePath)
print("SLOC:", len(rawCode))
