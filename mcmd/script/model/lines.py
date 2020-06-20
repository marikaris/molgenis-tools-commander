from typing import Set

import attr

from mcmd.script.model.statements import Statement


@attr.s(frozen=True)
class Line:
    number: int = attr.ib()
    string: str = attr.ib()


class ScriptLine:
    """
    A parsed line contains the line number, original line string and the parsed Statement. A parsed line may have
    dependencies on other lines (through Templates). These are exposed through the dependencies property.
    """

    def __init__(self, raw_string: str, number: int, statement: Statement):
        self._raw = raw_string
        self._number = number
        self._statement = statement
        self._dependencies = set()

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def number(self) -> int:
        return self._number

    @property
    def statement(self) -> Statement:
        return self._statement

    @property
    def dependencies(self) -> Set['ScriptLine']:
        return self._dependencies

    def add_dependency(self, line: 'ScriptLine'):
        self._dependencies.add(line)

    def __eq__(self, other):
        if isinstance(other, ScriptLine):
            if self._raw != other._raw: return False
            if self._number != other._number: return False
            if self._statement != other._statement: return False
            if self._dependencies != other._dependencies: return False
            return True
        else:
            return False

    def __key(self):
        return (self._raw, self._number)

    def __hash__(self):
        return hash(self.__key())
