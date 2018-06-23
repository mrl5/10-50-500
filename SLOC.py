#!/usr/bin/env python3

import sys
import RawCodeProvider

filePath = filePath = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
rawCode = RawCodeProvider.getRawCode(filePath)
print("SLOC:", len(rawCode))
