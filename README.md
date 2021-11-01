# Mobi reader

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MrLucio/mobi-reader/CI)
![PyPI - License](https://img.shields.io/pypi/l/mobi-reader)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mobi-reader)
![PyPI](https://img.shields.io/pypi/v/mobi-reader)

## Installation
```
  pip install mobi-reader
```

## Usage
This example is taken from [tests/test_reader.py](tests/test_reader.py)
```python
  from mobi import Mobi

  reader = Mobi('./alice_in_wonderland.mobi')
  output = reader.read()  # bytearray containing the decoded mobi file

  reader.close()
```
