# Mobi reader

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mobi-reader)
![PyPI](https://img.shields.io/pypi/v/mobi-reader)
![PyPI - License](https://img.shields.io/pypi/l/mobi-reader)

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
