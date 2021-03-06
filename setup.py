#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Extension
from babel.messages import frontend as babel

setup(
    name='ydict',
    version='1.0.0',
    description='Online Dictionary',
    long_description=''.join(open('README').readlines()),
    keywords='Chinese, English, Dictionary, Youdao',
    author='Wiky L',
    author_email='wiiiky@outlook.com',
    license='GPLv3',
    scripts=['bin/ydict.py'],
    url='https://github.com/wiiiky/ydict',
    packages=['pydict', 'pydict.youdao', 'pydict.base'],
    data_files=[
        ('/usr/share/icons/gnome/scalable/apps', ['data/ydict.svg']),
        ('/usr/share/applications', ['data/ydict.desktop'])
    ],
    package_dir={
        'pydict': 'pydict',
        'pydict.youdao': 'pydict/youdao',
        'pydict.glosbe': 'pydict/glosbe',
        'pydict.baidu': 'pydict/baidu',
        'pydict.base': 'pydict/base'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
    cmdclass={'compile_catalog': babel.compile_catalog,
              'extract_messages': babel.extract_messages,
              'init_catalog': babel.init_catalog,
              'update_catalog': babel.update_catalog}
)
