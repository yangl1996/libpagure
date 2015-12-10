# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='libpagure',
    packages=['libpagure'],
    version='0.6',
    description='A Python library for Pagure APIs.',
    author='Lei Yang',
    author_email='yltt1234512@gmail.com',
    url='https://github.com/yangl1996/libpagure',
    keywords=['pagure', 'api', 'library'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2 '
        'or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',

    ],
    license='GNU General Public License v2.0',
    install_requires=['requests'],
)
