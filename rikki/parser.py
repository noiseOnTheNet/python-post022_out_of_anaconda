#!/usr/bin/env python3

from yaml import load
from dataclasses import dataclass

@dataclass
class Deps:
    pip: [str]

@dataclass
class Environment:
    name: str
    dependencies: Deps
    prefix: str
