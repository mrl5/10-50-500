# -*- coding: utf-8 -*-

__author__ = "mrl5"

import os
import re


class Explorer:
    """
    Class for Maven project exploration
    """

    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.dirs = ['src', 'main', 'java']
        self.is_maven_project = False
        try:
            self.is_maven_project = self.verify_directory_layout(project_dir)
            self.source_dir = ''
            self.packages_dir = ''
            self.packages = dict()
            if self.is_maven_project:
                source_dir = project_dir
                for item in self.dirs:
                    source_dir = os.path.join(source_dir, item)
                self.source_dir = source_dir
                self.packages_dir = find_packages(source_dir)
        except FileNotFoundError as e:
            print(e.strerror, e.filename, sep=': ')
        except NotADirectoryError as e:
            print(e.strerror, e.filename, sep=': ')

    def verify_directory_layout(self, path):
        """
        Verifies if directory from path has Maven's "Standard Directory Layout" (src/main/java)
        :param path: path to Maven project
        :return: True if directory from path has Maven's "Standard Directory Layout"
        """
        errmsg = dict()
        for (i, item) in enumerate(self.dirs):
            if i == 0:
                errmsg[item] = "There is no \"" + item + "/\" dir."
            else:
                # append "src/" with next dir => "src/item/"
                errmsg[item] = re.sub(r'''
                                (       # start of grouping
                                [a-z]+  # match one or more small letters
                                /       # "/" character
                                )       # end of grouping
                                \"      # ending with "
                                ''', r'\1' + item + "/\"", errmsg[self.dirs[i - 1]], 0, re.VERBOSE)
        # check for Standard Directory Layout
        current_path = path
        for item in self.dirs:
            if find_dir(current_path, item):
                current_path = os.path.join(current_path, item)
            else:
                print(errmsg[item])
                # break loop, return False
                return False
        # return True if Maven's Standard Directory Layout
        return True

    def add_package(self, path):
        """
        Adds package and it's classes to the dictionary
        :param path: path to package
        :return: list with directories inside path
        """
        package_name = self.get_package_name(path)
        classes = list()
        directories = list()
        for item in os.listdir(path):
            path_to_item = os.path.join(path, item)
            if os.path.isfile(path_to_item) and item.endswith(".java"):
                classes.append(item)
            elif os.path.isdir(path_to_item):
                directories.append(path_to_item)
        if classes:
            self.packages[package_name] = classes
        return directories

    def get_package_name(self, path):
        """
        :param path: path to package
        :return: package name in accordance with Java packages naming convention
        """
        # get relative path to package
        relative_path = path.split(self.source_dir)[1]
        # remove first character (directory leftover)
        relative_path = re.sub(r'''
                            ^   # start of string
                            .   # any character (only one)
                            (   # start of grouping
                            .+  # one or more characters
                            $   # end of string
                            )   # end of grouping
                            ''', r'\1', relative_path, 0, re.VERBOSE)
        # convert relative path into Java package name
        package = re.sub('/', '.', relative_path, 0)
        return package

    def get_project_structure(self):
        """
        Creates a dictionary with packages and their classes ({package: [classes]})
        :return:
        """
        if not self.is_maven_project:
            print("Given path doesn't point to the Maven project", self.project_dir, sep=": ")
        else:
            paths_to_packages = list()
            paths_to_explore = list()
            for item in os.listdir(self.packages_dir):
                path_to_item = os.path.join(self.packages_dir, item)
                if os.path.isdir(path_to_item):
                    paths_to_explore.append(path_to_item)
            while len(paths_to_explore) > 0:
                paths_to_explore += self.add_package(paths_to_explore.pop(0))


def find_packages(path):
    """
    Searches for packages in given path
    :param path: path to dir which will be explored
    :return: path where java packages are located
    """
    packages_dir = path
    while len(os.listdir(packages_dir)) == 1:
        packages_dir = os.path.join(packages_dir, os.listdir(packages_dir)[0])

    return packages_dir


def find_dir(path, directory):
    """
    Searches for directory in given path
    :param path: path to main directory
    :param directory: name of searched directory
    :return: True if directory was found in path
    """
    for item in os.listdir(path):
        if item == directory and os.path.isdir(
                os.path.join(path, item)):
            return True


if __name__ == "__main__":
    import sys

    project_dir = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
    e = Explorer(project_dir)

    if not e.is_maven_project:
        print("Exiting with error")
    else:
        e.get_project_structure()
        for key in e.packages:
            print(key + ":")
            for value in e.packages[key]:
                print("\t" + value)
