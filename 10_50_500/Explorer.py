# -*- coding: utf-8 -*-

import os
import re

__author__ = "mrl5"


class Explorer:
    """
    Class for Maven project exploration
    """

    def __init__(self, project_dir=os.getcwd()):
        self.project_dir = project_dir
        self._packages = {}

    def _add_package(self, path):
        """
        Adds package and it's classes to the self._packages dictionary

        :param path: relative path to package (e.g. com/tuxnet/package)
        """
        package_classes = {}
        for item in os.listdir(path):
            path_to_item = os.path.join(os.path.abspath(path), item)
            if os.path.isfile(path_to_item):
                if os.path.basename(path_to_item).endswith(".java"):
                    java_class = {os.path.splitext(os.path.basename(path_to_item))[0]: path_to_item}
                    package_classes.update(java_class)
        # update self._packages only if package has .java files
        if bool(package_classes):
            package = {get_package_name(path): package_classes}
            self._packages.update(package)

    def get_project_structure(self):
        """
        :raises NotAMavenStandardDirectoryLayoutError: if a directory doesn't have Maven's "Standard Directory Layout" (src/main/java)
        :return: dictionary with java packages and their content (names and paths to classes)
        """
        if verify_directory_layout(self.project_dir):
            java_sources = os.path.join(self.project_dir, "src", "main", "java")
            # add packages to the set
            packages = set()
            for root, dirs, files in os.walk(java_sources, topdown=False):
                for f in files:
                    package = re.sub("{}{}".format("^", java_sources), '', root)
                    # //com/some/package -> com/some/package
                    package = re.sub("{}{}{}".format("^", os.sep, "+"), '', package)
                    packages.add(package)
            os.chdir(java_sources)
            # create dictionary of project
            for package in packages:
                self._add_package(package)
        else:
            raise self.NotAMavenStandardDirectoryLayoutError(filename=self.project_dir)
        return self._packages

    class NotAMavenStandardDirectoryLayoutError(Exception):
        """
        Custom exception for a directory which doesn't have Maven's "Standard Directory Layout" (src/main/java)
        """

        def __init__(self, **kwargs):
            self.strerror = "Directory doesn't have Maven's Standard Directory Layout (src/main/java)"
            self.filename = kwargs["filename"]


def verify_directory_layout(project_dir):
    """
    Verifies if directory from path has Maven's "Standard Directory Layout" (src/main/java)

    :param project_dir: path to the project
    :raises FileNotFoundError: when a directory is requested but doesn't exist
    :raises NotADirectoryError: when path leads to something which is not a directory
    :return: True if directory from path has Maven's "Standard Directory Layout"; else False
    """
    try:
        os.chdir(project_dir)
    except FileNotFoundError as fnfe:
        raise fnfe
    except NotADirectoryError as nade:
        raise nade

    maven_standard_directory_layout = os.path.join("src", "main", "java")
    path_to_analyse = os.path.join(project_dir, maven_standard_directory_layout)
    return os.path.exists(path_to_analyse)


def get_package_name(relative_package_path):
    """
    :param relative_package_path: relative path to package (e.g. com/tuxnet/package)
    :return: package name in accordance with Java packages naming convention
    """
    # //some/path//to/dir -> //some/path/to/dir
    path = os.path.normpath(relative_package_path)
    # //some/path/to/dir -> some/path/to/dir
    path = re.sub("{}{}{}".format("^", os.sep, "+"), '', path)
    # some/path/to/dir -> some.path.to.dir
    package = re.sub(os.sep, '.', path)
    return package


def main():
    project_dir = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
    explorer = Explorer(project_dir)
    try:
        explorer.get_project_structure()
        for package, files in sorted(explorer._packages.items()):
            print("\n", package, ":", sep='')
            for key, value in sorted(files.items()):
                print("\t" + key)
    except FileNotFoundError as e:
        print(e.strerror, e.filename, sep=': ')
    except NotADirectoryError as e:
        print(e.strerror, e.filename, sep=': ')
    except Explorer.NotAMavenStandardDirectoryLayoutError as e:
        print(e.strerror, e.filename, sep=': ')


if __name__ == "__main__":
    import sys
    main()
