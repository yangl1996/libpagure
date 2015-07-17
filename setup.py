from distutils.core import setup
setup(
    name='libpagure',
    packages=['libpagure'],
    version='0.21',
    description='A Python library for Pagure APIs.',
    author='Lei Yang',
    author_email='yltt1234512@gmail.com',
    url='https://github.com/yangl1996/libpagure',
    download_url='https://github.com/yangl1996/libpagure/tarball/0.21',
    keywords=['pagure', 'api', 'library'],
    classifiers=[
        'Programming Language :: Python',
    ],
    license='GNU General Public License v2.0',
    install_requires=['requests'],
)
