from typing import Union, List
from dataclasses import dataclass

@dataclass
class Constr:
    version: Union[List[int],str]
    operator: str

@dataclass
class Dep:
    package: str
    constraints: [Constr]

@dataclass
class Environment:
    name: str
    deps: [Dep]
    prefix: str
