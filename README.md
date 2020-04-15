<h1 align="center">pyartifacts</h1>

<p  align="center">
 <a href="https://github.com/forensicanalysis/pyartifacts/actions"><img src="https://github.com/forensicanalysis/pyartifacts/workflows/CI/badge.svg" alt="build" /></a>
 <a href="https://codecov.io/gh/forensicanalysis/pyartifacts"><img src="https://codecov.io/gh/forensicanalysis/pyartifacts/branch/master/graph/badge.svg" alt="coverage" /></a>
 <a href='https://pyartifacts.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/pyartifacts/badge/?version=latest' alt='Documentation Status' /></a>
</p>


The pyartifacts project provides a Python library for processing
forensic artifact definition files.

## Artifact definition files
The artifact definition format is described in detail in the Style Guide ([https://github.com/forensicanalysis/artifacts/blob/master/style_guide.md](https://github.com/forensicanalysis/artifacts/blob/master/style_guide.md)).
The following shows an example for an artifact definition file. It defines the
location of linux audit log files on a system.

```
name: LinuxAuditLogFiles
doc: Linux audit log files.
sources:
- type: FILE
  attributes: {paths: ['/var/log/audit/*']}
supported_os: [Linux]
```

We use [https://github.com/forensicanalysis/artifacts](https://github.com/forensicanalysis/artifacts) as the main repository for
forensic artifacts definitions.

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
