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
    - only .java files from the first level should be added
    - don't create dictionary for empty package

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
    assert verify_directory_layout(str(test_project)) is True


def test_false_directory_layout(tmpdir):
    test_project = tmpdir.mkdir("test_project")
    os.makedirs(os.path.join(str(test_project), "some", "random", "dir"))
    assert verify_directory_layout(str(test_project)) is False


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


# self.add_package
def test_add_package(explorer, tmpdir):
    package_dir = tmpdir.mkdir("com").mkdir("package")
    some_dir = "some_dir"
    os.mkdir(os.path.join(str(package_dir), some_dir))
    package_name = get_package_name(str(package_dir))
    java_classes = {}
    test_item = {package_name: java_classes}
    for java_class in '12345':
        java_file = str("{}.{}").format(java_class, "java")
        some_file = str("{}.{}").format(java_class, "txt")
        os.mknod(os.path.join(str(package_dir), java_file))
        os.mknod(os.path.join(str(package_dir), some_file))
        os.mknod(os.path.join(str(package_dir), some_dir, java_file))
        os.mknod(os.path.join(str(package_dir), some_dir, some_file))
        java_classes.update({java_class: os.path.join(str(package_dir), java_file)})
    explorer._add_package(str(package_dir))
    assert test_item[package_name] == explorer._packages[package_name]


def test_empty_package(explorer, tmpdir):
    package_dir = tmpdir.mkdir("com").mkdir("package")
    package_name = get_package_name(str(package_dir))
    java_classes = {}
    test_item = {package_name: java_classes}
    explorer._add_package(str(package_dir))
    with pytest.raises(KeyError):
        print(explorer._packages[package_name])
