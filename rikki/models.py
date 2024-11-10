from typing import Union, List
from dataclasses import dataclass

@dataclass
class Constr:
    version: Union[List[int],str]
    operator: str
    def get_str_version(self):
        if type(self.version) == str:
            return self.version
        else:
            return ".".join([str(i) for i in self.version])

@dataclass
class Dep:
    package: str
    constraints: List[Constr]

@dataclass
class Environment:
    name: str
    deps: List[Dep]
    prefix: str

@dataclass
class Requirements:
    deps: List[Dep]
