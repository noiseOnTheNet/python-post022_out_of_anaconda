#!/usr/bin/env python3

import rikki.parser
from pathlib import Path
import pytest

DIR = Path(__file__).parent

def test_parse():

    result = rikki.parser.read(DIR / "lite_full.yaml")
    assert result is not None
    assert isinstance(result, rikki.parser.Environment)
    assert len(result.deps) == 120

@pytest.mark.parametrize(
    "value,package,version",[
        ("_libgcc_mutex=0.1=main", "_libgcc_mutex", [0,1]),
        ("tk=8.6.12=h1ccaba5_0", "tk", [8,6,12]),
        ("tzdata=2024a=h04d1e81_0", "tzdata", "2024a"),
    ]
)
def test_parse_conda_constr(value,package,version):
    result = rikki.parser.parse_conda_dep(value)
    assert result.package == package
    assert result.constraints[0].version == version


@pytest.mark.parametrize(
    "value,package,version,operator",[
        ("anyio==4.3.0", "anyio", [4,3,0], "=="),
        ("argon2-cffi==23.1.0", "argon2-cffi", [23, 1, 0], "==")
    ]
)
def test_parse_pip_constr(value,package,version,operator):
    result = rikki.parser.parse_pip_dep(value)
    assert result.package == package
    assert result.constraints[0].version == version
    assert result.constraints[0].operator == operator
