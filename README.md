# libpagure

A Python library for Pagure APIs. Pagure is a light-weight git-centered forge based on pygit2, created by Pierre-Yves Chibon.

## Docker Development environment

To build the development environment we provide a Dockerfile. You can build the container as follow:

    $ cd devel
    $ docker build -t libpagure_dev .
    $ cd ..

Once the container is built you can run the tests using the following command for Python 3.6

    $ docker run -it --rm -v `pwd`:/code:z libpagure_dev py.test-3.6 --cov libpagure

and for Python 2.7.

    $ docker run -it --rm -v `pwd`:/code:z libpagure_dev py.test-2.7 --cov libpagure

You can also run an interactive shell inside the container using:

    $ docker run -it --rm -v `pwd`:/code:z libpagure_dev

In each case `pwd` command needs to return the root path of libpagure repository. (ie where this readme is)

## Running the unit tests outside the Docker environment

First you need to install the dependencies needed ::

    $ sudo dnf install python2-requests python3-requests python2-flake8\
    python3-flake8 python2-pytest python3-pytest python3-pytest-cov\
    python2-pytest-cov python2-pytest-mock python3-pytest-mock

Then you can execute the test suite using the following commands for Python 2.7 and 3.6. ::

    $ py.test-3.6 --cov libpagure
    $ py.test-2.7 --cov libpagure

## Installation
---

Use pip to install.

### Linux
---

```
pip3 install libpagure
```

### OS X
---

```
python3 -m pip install libpagure
```

## Usage
---
* Import and Initialization:
```
>>> from libpagure import Pagure
>>> pg = Pagure()
```

* Get the API version
```
>>> pg.api_version()
'0.8'
```

* Create a new Project
```
>>> from libpagure import Pagure
>>> pg = Pagure(pagure_token="foobar")
>>> pg.new_project(name="foo", description="bar", url="http://foobar.io",
                   create_readme=True)
>>> Project "foo" created
```

This library is a Python wrapper of Pagure web APIs.
You can refer to [Pagure API](https://pagure.io/api/0/) reference.
