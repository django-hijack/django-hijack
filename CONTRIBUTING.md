# Contributing Guide

## Setup Development Environment

### Non-Python dependencies

You will need both a supported version of Node.js and gettext.
Gettext is best installed using a package manager like apt or brew.

```shell
# Debian/Ubuntu
sudo apt install gettext
# macOS
brew install gettext
```

You may use NVM to install the correct Node.js version:

```shell
nvm install
nvm use
```

### Development setup

After installing the non-Python dependencies, its as easy as calling:

```shell
python -m pip install -e '.[test]'
```

## Tests

Simply run:

```shell
py.test
```
