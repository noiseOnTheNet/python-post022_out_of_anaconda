"""parser library to read conda environment data"""
import re
from pathlib import Path
from yaml import load, CLoader as Loader
from typing import Union, List
from .models import Constr, Dep, Environment

def read(filename: Union[str,Path]):
    with open(filename) as f:
        base_dict = load(f, Loader)
        deps = []
        for dep in base_dict['dependencies']:
            if type(dep) == str:
                deps.append(parse_conda_dep(dep))
            elif type(dep) == dict:
                for pip_dep in dep['pip']:
                    deps.append(parse_pip_dep(pip_dep))
            else:
                raise Exception(f"unknown dependency type '{dep}' : {type(dep)}")
        return Environment(name=base_dict['name'],deps=deps,prefix=base_dict['prefix'])

CONDA_RE = re.compile(r"(?P<package>[^=]+)=+(?P<version>[^=]+)")

def parse_conda_dep(value: str):
    matching = CONDA_RE.match(value)
    assert matching is not None, f"cannot parse conda dependency {value}"
    groups = matching.groupdict()
    version=parse_version(groups['version'])
    return Dep(
        package=groups['package'],
        constraints=[
            Constr(
                version=version,
                operator='=='
            )
        ]
    )

def parse_version(value: str):
    try:
        version = [int(i) for i in value.split('.')]
    except ValueError:
        version = value
    return version

PIP_RE = re.compile(r"(?P<package>[_A-Za-z0-9\-]+)(?P<constraints>.*)")
PIP_CONSTRAINT = re.compile(r"(?P<operator>[=~\^><]+)(?P<version>.*)")

def parse_pip_dep(value: str):
    dep_matching = PIP_RE.match(value)
    assert dep_matching is not None, f"cannot parse pip dependency {value}"
    dep_groups = dep_matching.groupdict()
    constraints = []
    for c in dep_groups['constraints'].split(','):
        constr_matching = PIP_CONSTRAINT.match(c)
        assert constr_matching is not None, f"cannot parse pip constraint {c} in {value}"
        constr_groups = constr_matching.groupdict()
        version = parse_version(constr_groups['version'])
        constraints.append(
            Constr(
                version = version,
                operator = constr_groups['operator']
            )
        )
    return Dep(
        package = dep_groups['package'],
        constraints = constraints
    )
