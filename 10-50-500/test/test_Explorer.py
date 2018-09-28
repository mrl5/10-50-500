# -*- coding: utf-8 -*-

import pytest
import os

__author__ = "mrl5"

from Explorer import Explorer, verify_directory_layout, get_package_name

"""
Scenario:
1) test if Explorer can be instantiated

2) test 'verify_directory_layout' function for checking Maven's "Standard Directory Layout" (src/main/java)
    - if correct layout: return True
    - if project doesn't have "Standard Directory Layout": return False
    - if path doesn't exist throw "FileNotFoundError" exception
    - if path leads to file throw "NotADirectoryError" exception

3) test 'get_package_name' function: input relative path to package; output package name (Java packages naming convention)
    - /com/company/package -> com.company.package
    - //com/company//package -> com.company.package
    
4) test 'add_package' method:
    - method should add new item to the dictionary (named as package) with all filenames and full paths to the .java files

5) test 'get_project_structure' method:
    - if project doesn't have "Standard Directory Layout": throw "NotAStandardDirectoryLayout" exception
    - on "FileNotFoundError" exception: print error
    - on "NotADirectoryError" exception: print error
    - if "Standard Directory Layout": fill 'self.packages' dictionary with structure "{package: {class: path/to/class}}"
"""


@pytest.fixture()
def explorer():
    explorer = Explorer()
    return explorer


# verify_directory_layout
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


# get_package_name
def test_get_package_name():
    path_to_package = os.path.join(os.sep, "com", "tuxnet", "package")
    assert get_package_name(path_to_package) == "com.tuxnet.package"


def test_multi_sep_package_name():
    path_to_package = os.path.join(os.sep, "com", "tuxnet", "package")
    path = "{}{}".format(os.sep, path_to_package)
    assert get_package_name(path) == "com.tuxnet.package"
