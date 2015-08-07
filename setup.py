#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages, Extension
except:
    from distutils.core import setup, find_packages, Extension


setup(
    name='ydict',
    version='0.2.0',
    description='Online Dictionary',
    long_description=''.join(open('README').readlines()),
    keywords='Chinese, English, Dictionary, Youdao',
    author='Wiky L',
    author_email='wiiiky@outlook.com',
    license='GPLv3',
    scripts=['bin/ydict.py'],
    packages=['pydict', 'pydict.youdao', 'pydict.base'],
    package_dir={
        'pydict': 'pydict',
        'pydict.youdao': 'pydict/youdao',
        'pydict.base': 'pydict/base'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
)
