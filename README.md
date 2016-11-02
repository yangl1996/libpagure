# libpagure

A Python library for Pagure APIs. Pagure is a light-weight git-centered forge based on pygit2, created by Pierre-Yves Chibon.

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
>>> pg.new_project(name="foo", description="bar", url="http://foobar.io", create_readme=True)
>>> Project "foo" created
```

This library is a Python warp of Pagure web APIs, so you may refer to [Pagure API](https://pagure.io/api/0/) reference.
