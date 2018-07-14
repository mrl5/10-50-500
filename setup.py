# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='10-50-500',
    version='0.1.0',
    description='Check maven project against 10-50-500 rule',
    long_description=readme,
    author='mrl5',
    author_email='secret',
    url='https://github.com/mrl5/10-50-500',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
