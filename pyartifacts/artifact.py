# Copyright (c) 2019 Siemens AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Author(s): Demian Kellermann

# pylint: disable=too-few-public-methods

""" Classes that represent artifacts and parts of them """

import logging
from typing import List, Dict

from .definitions import SOURCE_TYPE_ARTIFACT_GROUP, SOURCE_TYPE_COMMAND, SOURCE_TYPE_DIRECTORY, SOURCE_TYPE_FILE, \
    SOURCE_TYPE_PATH, SOURCE_TYPE_REGISTRY_KEY, SOURCE_TYPE_REGISTRY_VALUE, SOURCE_TYPE_WMI
from .variables import get_needed_vars

LOGGER = logging.getLogger(__name__)


class SourceProvide:
    """ Represents a source provides entry """

    def __init__(self, key: str, regex: str = None, wmi_key: str = None):
        self.key = key
        self.regex = regex
        self.wmi_key = wmi_key

    def __repr__(self):
        return 'SourceProvides(' + self.key + ')'


class ArtifactSource:
    """ Abstract base class for artifact source definitions """

    def __init__(self, source_type: str, provides: List[SourceProvide] = None, supported_os: List[str] = None):
        self.type = source_type
        self.provides = provides or []
        self.needs = set()
        self.supported_os = supported_os or []

    def __repr__(self):
        return self.type


class ArtifactDefinition:
    """ Base class for artifacts """

    def __init__(self, name: str, sources: List[ArtifactSource],
                 aliases: List[str] = None, supported_os: List[str] = None):
        self.name = name
        self.sources = sources
        self.aliases = aliases or []
        self.supported_os = supported_os or []

    def __repr__(self):
        return f'Artifact({self.name}, {len(self.sources)} sources, {self.supported_os})'


class ArtifactGroupSource(ArtifactSource):
    """ ARTIFACT_GROUP """

    def __init__(self, names: List[str], supported_os: List[str] = None):
        super().__init__(source_type=SOURCE_TYPE_ARTIFACT_GROUP, supported_os=supported_os)
        self.names = names


class ArtifactCommandSource(ArtifactSource):
    """ COMMAND """

    def __init__(self, cmd: str, args: List[str] = None, provides: List[SourceProvide] = None,
                 supported_os: List[str] = None):
        super().__init__(source_type=SOURCE_TYPE_COMMAND, provides=provides, supported_os=supported_os)
        self.cmd = cmd
        self.args = args or []
        self.needs.update(get_needed_vars(self.cmd))
        self.needs.update(get_needed_vars(*self.args))


class ArtifactFilesystemSource(ArtifactSource):
    """ DIRECTORY, FILE and PATH """

    def __init__(self, source_type: str, paths: List[str], separator: str = None, provides: List[SourceProvide] = None,
                 supported_os: List[str] = None):
        super().__init__(source_type=source_type, provides=provides, supported_os=supported_os)
        self.paths = paths
        self.separator = separator
        self.needs.update(get_needed_vars(*self.paths))


class ArtifactRegistryKeySource(ArtifactSource):
    """ REGISTRY_KEY """

    def __init__(self, keys: List[str], provides: List[SourceProvide] = None, supported_os: List[str] = None):
        super().__init__(source_type=SOURCE_TYPE_REGISTRY_KEY, provides=provides, supported_os=supported_os)
        self.keys = keys
        self.needs.update(get_needed_vars(*self.keys))


class ArtifactRegistryValueSource(ArtifactSource):
    """ REGISTRY_VALUE """

    def __init__(self, key_value_pairs: List[Dict[str, str]], provides: List[SourceProvide] = None,
                 supported_os: List[str] = None):
        super().__init__(source_type=SOURCE_TYPE_REGISTRY_VALUE, provides=provides, supported_os=supported_os)
        self.key_value_pairs = key_value_pairs
        for path in (kvp['key'] for kvp in self.key_value_pairs):
            self.needs.update(get_needed_vars(path))


class ArtifactWMISource(ArtifactSource):
    """ WMI """

    def __init__(self, query: str, base_object: str = None, provides: List[SourceProvide] = None,
                 supported_os: List[str] = None):
        super().__init__(source_type=SOURCE_TYPE_WMI, provides=provides, supported_os=supported_os)
        self.query = query
        self.base_object = base_object
        self.needs.update(get_needed_vars(self.query))


def make_artifact(artifact_yaml: dict) -> ArtifactDefinition:
    """ Parses a dict into an ArtifactDefinition object """
    LOGGER.debug("Making artifact %s...", artifact_yaml.get('name', 'WTF NO NAME'))
    name = artifact_yaml['name']
    supported_os = artifact_yaml.get('supported_os', [])
    aliases = artifact_yaml.get('aliases', [])
    sources_dict = artifact_yaml['sources']
    sources = []
    for source_dict in sources_dict:
        source_type = source_dict['type']
        provides = []
        provides_dict = source_dict.get('provides', [])
        for provide_dict in provides_dict:
            provides.append(SourceProvide(**provide_dict))
        source_os = source_dict.get('supported_os', [])

        if source_type in (SOURCE_TYPE_DIRECTORY, SOURCE_TYPE_FILE, SOURCE_TYPE_PATH):
            sources.append(ArtifactFilesystemSource(
                source_type,
                provides=provides,
                supported_os=source_os,
                **source_dict['attributes'],
            ))
        elif source_type == SOURCE_TYPE_ARTIFACT_GROUP:
            sources.append(ArtifactGroupSource(supported_os=source_os, **source_dict['attributes']))
        elif source_type == SOURCE_TYPE_WMI:
            sources.append(
                ArtifactWMISource(provides=provides, supported_os=source_os, **source_dict['attributes']))
        elif source_type == SOURCE_TYPE_REGISTRY_VALUE:
            sources.append(
                ArtifactRegistryValueSource(provides=provides, supported_os=source_os, **source_dict['attributes']))
        elif source_type == SOURCE_TYPE_REGISTRY_KEY:
            sources.append(
                ArtifactRegistryKeySource(provides=provides, supported_os=source_os, **source_dict['attributes']))
        elif source_type == SOURCE_TYPE_COMMAND:
            sources.append(
                ArtifactCommandSource(provides=provides, supported_os=source_os, **source_dict['attributes']))
        else:
            raise ValueError(f"{name}: Unknown source type: {source_type}")
    artifact = ArtifactDefinition(name, sources, aliases, supported_os)
    return artifact
