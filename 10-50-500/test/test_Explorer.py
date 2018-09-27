# -*- coding: utf-8 -*-

import pytest
import os

__author__ = "mrl5"

from Explorer import Explorer, verify_directory_layout

"""
Scenario:
1) test if Explorer can be instantiated

2) test 'verify_directory_layout' function for checking Maven's "Standard Directory Layout" (src/main/java)
    - if correct layout: return True
    - if project doesn't have "Standard Directory Layout": return False
    - if path doesn't exist throw "FileNotFoundError" exception
    - if path leads to file throw "NotADirectoryError" exception

3) test 'get_package_name' method: input relative path to package; output package name (Java packages naming convention)
    (eg. /com/company/package -> com.company.package)
    
4) test 'get_project_structure' method: fill 'self.packages' dictionary with structure "{package: {class: path/to/class}}"
"""

@pytest.fixture()
def explorer():
    explorer = Explorer()
    return explorer


def test_correct_directory_layout(tmpdir):
    test_project = tmpdir.mkdir("test_project")
    os.makedirs(os.path.join(str(test_project), "src", "main", "java"))
    assert verify_directory_layout(str(test_project)) == True


def test_false_directory_layout(tmpdir):
    test_project = tmpdir.mkdir("test_project")
    os.makedirs(os.path.join(str(test_project), "some", "random", "dir"))
    assert verify_directory_layout(str(test_project)) == False


def test_path_doesnt_exist(tmpdir):
    test_dir = tmpdir.mkdir("test_dir")
    imaginary_project =  os.path.join(str(test_dir), "imaginary", "project")
    with pytest.raises(FileNotFoundError):
        verify_directory_layout(imaginary_project)


def test_path_to_file(tmpdir):
    imaginary_project = tmpdir.mkdir("test_dir").join("im_file.txt")
    imaginary_project.write("content")
    print(str(imaginary_project))
    with pytest.raises(NotADirectoryError):
        verify_directory_layout(str(imaginary_project))