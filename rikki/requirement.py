from pathlib import Path
from .models import Environment, Requirements
from typing import Union

def env_to_requirement(env: Environment):
    return Requirements(deps=env.deps)

def dump_requirements(reqs: Requirements):
    for dep in reqs.deps:
       yield "{}{}".format(
           dep.package,
           ",".join([
               "{}{}".format(
                   c.operator,
                   c.get_str_version()
               )
               for c in dep.constraints
           ])
       )


def write_requirements(reqs: Requirements, path: Union[str,Path]):
    with open(path, mode="tw") as f:
        for line in dump_requirements(reqs):
            print(line,file=f)
