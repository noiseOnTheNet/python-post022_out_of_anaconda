import rikki.parser
import rikki.requirement
from rikki.models import Constr
from pathlib import Path

DIR = Path(__file__).parent

def test_version():
    fixture = Constr(operator="==",version=[1,2,3])
    expected = "1.2.3"
    assert fixture.get_str_version() == expected

def test_dump():
    result = rikki.parser.read(DIR / "lite_full.yaml")
    result = list(rikki.requirement.dump_requirements(result))
    assert len(result) == 120
    print(result)
    for line in result:
        print(line)
        matching  = rikki.parser.PIP_RE.match(line)
        assert matching is not None
        constraints = matching.groupdict()['constraints']
        for c in constraints.split(','):
            assert rikki.parser.PIP_CONSTRAINT.match(c) is not None
