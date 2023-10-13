from construct_base import ConstructBase
from str_construct_exceptions import StrConstructParseError

class StrConst(ConstructBase):
    def __init__(self, const):
        self.name = None
        self._const = const

    def _build(self, value):
        if value is not None and value != self._const:
            raise ValueError("StrConst needs the same constant value or nothing to build")

        return self._const

    def _parse(self, string):
        if not string.startswith(self._const):
            raise StrConstructParseError(f"Expected '{self._const}' but found '{string}'")
        self._parse_left = string[len(self._const) :]
        return self._const
