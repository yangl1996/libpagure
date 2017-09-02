# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_install_requires():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f]


def get_test_requires():
    with open('test-requirements.txt', 'r') as f:
        return [line.strip() for line in f if not line.startswith('-r ')]


setup(
    name='libpagure',
    packages=['libpagure'],
    version='0.9',
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
    install_requires=get_install_requires(),
    test_requires=get_test_requires(),
)
