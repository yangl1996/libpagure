from distutils.core import setup
setup(
    name = 'libpagure',
    packages = ['libpagure'], # this must be the same as the name above
    version = 'v0.11',
    description = 'A Python library for Pagure APIs.',
    author = 'Lei Yang',
    author_email = 'yltt1234512@gmail.com',
    url = 'https://github.com/yangl1996/libpagure', # use the URL to the github repo
    download_url = 'https://github.com/yangl1996/libpagure/tarball/v0.11', # I'll explain this in a second
    keywords = ['pagure', 'api', 'library'], # arbitrary keywords
    classifiers = ['Programming Language :: Python'],
    license = "GNU General Public License v2.0"
)