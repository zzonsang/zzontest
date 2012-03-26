#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from setuptools import setup
from setuptools.command.install_lib import install_lib as _install_lib
import setuptools
from vdi_report import __vendor__, __version__

class install_lib(_install_lib):
    def byte_compile(self, files):
        _install_lib.byte_compile(self, files)
        for f in files:
            os.unlink(f)
setuptools.command.install_lib.install_lib = install_lib

def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
    except IOError:
        return ''
    
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

def datafiles():
    data_files = []    
    data_paths = {'vdi_report/templates' }
    
    for data_path in data_paths:
        for dirpath, dirnames, filenames in os.walk(data_path):        
            for i, dirname in enumerate(dirnames):
                if dirname.startswith('.'): del dirnames[i]
            if filenames:
                data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return data_files

setup(name='Weekly Report',
    version=__version__,
    description='Weelky Report',
    long_description=read('README_server'),
    author=__vendor__,
    author_email='zzonsang2@gmail.com',
    platforms=['Any'],
    packages=['vdi_report'],
    data_files = datafiles(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django==1.3', 
        'django-grappelli'
    ],
)
