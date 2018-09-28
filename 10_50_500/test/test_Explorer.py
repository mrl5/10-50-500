# -*- coding: utf-8 -*-

import pytest
import os
import re

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
    
4) test '_add_package' method:
    - method should add new item to the dictionary (named as package) with all filenames and full paths to the .java files
    - only .java files from the first level should be added
    - don't create dictionary for empty package

5) test 'get_project_structure' method:
    - if project doesn't have "Standard Directory Layout": throw "NotAMavenStandardDirectoryLayoutError" exception
    - don't handle 'verify_directory_layout' exceptions
    - if "Standard Directory Layout": retunr 'self._packages' dictionary with structure "{package: {class: path/to/class}}"
"""


@pytest.fixture(scope="function")
def explorer():
    explorer = Explorer()
    return explorer


@pytest.fixture(scope="function")
def maven_sdl(tmpdir):
    test_project = tmpdir.mkdir("test_project")
    os.makedirs(os.path.join(str(test_project), "src", "main", "java"))
    return test_project


class ProjectDirectory:
    def __init__(self, maven_sdl):
        self.directory = maven_sdl
        self.java_sources = os.path.join(str(self.directory), "src", "main", "java")
        pkg_one = os.path.join(self.java_sources, "com", "tuxnet", "p_one")
        pkg_two = os.path.join(pkg_one, "p_two")
        pkg_three = os.path.join(self.java_sources, "com", "tuxnet", "p_three")
        self.pkgs = ["com.tuxnet.p_one", "com.tuxnet.p_one.p_two", "com.tuxnet.p_three"]
        self.packages = {pkg: [pkg_one, pkg_two, pkg_three][i] for i, pkg in enumerate(self.pkgs)}
        self.test_files_string = '12'

    def setup_project(self):
        """
        Sets up test directory containing Maven project structure
        """
        os.makedirs(os.path.join(str(self.directory), "some", "random", "dir"))
        # for each package create sample files
        for package_name, package_path in self.packages.items():
            # necessary if com/tuxnet/p_one/p_two was created before com/tuxnet/p_one
            try:
                os.makedirs(package_path)
            except FileExistsError:
                pass
            for java_class in self.test_files_string:
                java_file = str("{}.{}").format(java_class, "java")
                some_file = str("{}.{}").format(java_class, "txt")
                os.mknod(os.path.join(package_path, java_file))
                os.mknod(os.path.join(str(package_path), some_file))


@pytest.fixture(scope="function")
def maven_test_project(maven_sdl):
    maven_project = ProjectDirectory(maven_sdl)
    maven_project.setup_project()
    return maven_project


# verify_directory_layout
def test_correct_directory_layout(maven_sdl):
    test_directory = maven_sdl
    assert verify_directory_layout(str(test_directory)) is True


def test_false_directory_layout(tmpdir):
    test_directory = tmpdir.mkdir("test_project")
    os.makedirs(os.path.join(str(test_directory), "some", "random", "dir"))
    assert verify_directory_layout(str(test_directory)) is False


def test_path_doesnt_exist(tmpdir):
    test_directory = tmpdir.mkdir("test_dir")
    imaginary_project = os.path.join(str(test_directory), "imaginary", "project")
    with pytest.raises(FileNotFoundError):
        verify_directory_layout(imaginary_project)


def test_path_to_file(tmpdir):
    imaginary_project = tmpdir.mkdir("test_dir").join("im_file.txt")
    imaginary_project.write("content")
    with pytest.raises(NotADirectoryError):
        verify_directory_layout(str(imaginary_project))


# get_package_name
def test_get_package_name():
    dirs = ["com", "tuxnet", "package"]
    path_to_package = os.path.join(os.sep, dirs[0], dirs[1], dirs[2])
    # com.tuxnet.package
    assert get_package_name(path_to_package) == ".".join(dirs)


def test_multi_sep_package_name():
    dirs = ["com", "tuxnet", "package"]
    path_to_package = os.path.join(os.sep, dirs[0], dirs[1], dirs[2])
    path = "{}{}".format(os.sep, path_to_package)
    # com.tuxnet.package
    assert get_package_name(path) == ".".join(dirs)


# self._add_package
def test_add_package(explorer, maven_test_project):
    # make sure that the cwd is relative
    os.chdir(maven_test_project.java_sources)
    package_name = maven_test_project.pkgs[0]
    package_dir = maven_test_project.packages[package_name]
    relative_package_dir = re.sub("{}{}{}".format("^", maven_test_project.java_sources, os.sep), '', package_dir)

    java_classes = {}
    synthetic_result = {package_name: java_classes}
    for item in os.listdir(relative_package_dir):
        item_path = os.path.join(relative_package_dir, item)
        if os.path.isfile(item_path) and item.endswith(".java"):
            java_class = os.path.basename(item)[0]
            # make sure to provide full absolute path
            abs_path_to_class = os.path.join(os.path.abspath(maven_test_project.java_sources), relative_package_dir, item)
            java_classes.update({java_class: abs_path_to_class})

    explorer._add_package(relative_package_dir)
    assert synthetic_result[package_name] == explorer._packages[package_name]


def test_empty_package(explorer, tmpdir):
    package_dir = tmpdir.mkdir("com").mkdir("package")
    package_name = get_package_name(str(package_dir))

    explorer._add_package(str(package_dir))
    with pytest.raises(KeyError):
        print(explorer._packages[package_name])


# self.get_project_structure
def test_NotAMavenStandardDirectoryLayoutError_exception(explorer, tmpdir):
    test_project = tmpdir.mkdir("test_project")
    os.makedirs(os.path.join(str(test_project), "some", "random", "dir"))

    explorer.project_dir = str(test_project)
    with pytest.raises(explorer.NotAMavenStandardDirectoryLayoutError):
        explorer.get_project_structure()


def test_get_project_structure(explorer, maven_test_project):
    synthetic_result = {maven_test_project.pkgs[0]: {}, maven_test_project.pkgs[1]: {}, maven_test_project.pkgs[2]: {}}
    for package_name, package_path in maven_test_project.packages.items():
        package_classes = {}
        for java_class in maven_test_project.test_files_string:
            java_file = str("{}.{}").format(java_class, "java")
            package_classes.update({java_class: os.path.join(os.path.abspath(package_path), java_file)})
        synthetic_result[package_name].update(package_classes)

    explorer.project_dir = str(maven_test_project.directory)
    assert explorer.get_project_structure() == synthetic_result
