# -*- coding: utf-8 -*-

import pytest

__author__ = "mrl5"

"""
Scenario:
1) test if Explorer can be instantiated

2) test 'verify_directory_layout' method for checking Maven's "Standard Directory Layout" (src/main/java)
    - if project doesn't have "Standard Directory Layout" throw "NotAStandardDirectoryLayoutError" exception
    - if path doesn't exist throw "FileNotFoundError" exception
    - if path leads to file throw "NotADirectoryError" exception

3) test 'get_package_name' method: input relative path to package; output package name (Java packages naming convention)
    (eg. com/company/package -> com.company.package)
    
4) test 'get_project_structure' method: fill 'self.packages' dictionary with structure "{package: {class: path/to/class}}"
"""