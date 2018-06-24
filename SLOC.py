#!/usr/bin/env python

__author__ = "mrl5"

import sys
import RawCodeProvider

file_path = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
raw_code = RawCodeProvider.get_raw_code(file_path)
print("SLOC: {}".format(len(raw_code)))
