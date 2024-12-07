# pygenv


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

Mainly a way to test the `nbdev` experience but also answering [this
question](https://bsky.app/profile/howard.fm/post/3lch556wehc24):

> For folks that don’t use conda, how do you debug problems that only
> occur on some particular Python or CUDA version?
>
> With conda, I have a few envs set up with various python and CUDA
> versions, so I just activate one and get to work.
>
> With something like uv, what do you do?

## Developer Guide

If you are new to using `nbdev` here are some useful pointers to get you
started.

### Install pygenv in Development mode

``` sh
# make sure pygenv package is installed in development mode
$ pip install -e .

# make changes under nbs/ directory
# ...

# compile to have changes apply to pygenv
$ nbdev_prepare
```

## Usage

### Installation

Install latest from the GitHub
[repository](https://github.com/tkukurin/pygenv):

``` sh
$ pip install git+https://github.com/tkukurin/pygenv.git
```

or from [conda](https://anaconda.org/tkukurin/pygenv)

``` sh
$ conda install -c tkukurin pygenv
```

or from [pypi](https://pypi.org/project/pygenv/)

``` sh
$ pip install pygenv
```

### Documentation

Documentation can be found hosted on this GitHub
[repository](https://github.com/tkukurin/pygenv)’s
[pages](https://tkukurin.github.io/pygenv/). Additionally you can find
package manager specific guidelines on
[conda](https://anaconda.org/tkukurin/pygenv) and
[pypi](https://pypi.org/project/pygenv/) respectively.