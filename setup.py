# coding=utf-8
from setuptools import setup

setup(
    name = 'python-transform',
    py_modules = ['transform'],
    #test_suite = 'test',
    version = '0.0.1',
    description = 'transform a python datatructure into another using a set of rules.',
    long_description = open('README').read(),
    url = 'http://github.com/clement/python-transform',
    author = 'Clément Nodet',
    author_email = 'clement.nodet@gmail.com',
    classifiers = [ 'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2',
                    'Development Status :: 2 - Pre-Alpha',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                    'Topic :: Software Development :: Libraries :: Python Modules' ]
)
