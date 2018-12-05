import yaml
from collections import OrderedDict

from apispec.lazy_dict import LazyDict
from apispec.core import Path

from app.models.model_registrar import spec


def represent_dict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())


yaml.add_representer(OrderedDict, represent_dict)
yaml.add_representer(LazyDict, represent_dict)
yaml.add_representer(Path, represent_dict)

for definition in spec.to_dict()['definitions']:
    with open('docs/definitions/' + definition + ".yaml", 'w') as outfile:
        yaml.dump(spec.to_dict()['definitions'][definition], outfile, default_flow_style=False)
