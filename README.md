<h1 align="center">pyartifacts</h1>

<p  align="center">
 <a href="https://github.com/forensicanalysis/pyartifacts/actions"><img src="https://github.com/forensicanalysis/pyartifacts/workflows/CI/badge.svg" alt="build" /></a>
 <a href="https://codecov.io/gh/forensicanalysis/pyartifacts"><img src="https://codecov.io/gh/forensicanalysis/pyartifacts/branch/master/graph/badge.svg" alt="coverage" /></a>
 <a href='https://pyartifacts.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/pyartifacts/badge/?version=latest' alt='Documentation Status' /></a>
</p>


The pyartifacts project provides a Python library for processing
forensic artifact definition files.


### Installation

Python installation can be easily done via pip:

```bash
pip install pyartifacts
```

### Usage

```python
from pyartifacts.registry import Registry

if __name__ == '__main__':
    registry = Registry()
    registry.read_folder("test/artifacts/valid")
    print(registry)
```

## Contact

For feedback, questions and discussions you can use the [Open Source DFIR Slack](https://github.com/open-source-dfir/slack).

## Acknowledgment

The development of this software was partially sponsored by Siemens CERT, but
is not an official Siemens product.
