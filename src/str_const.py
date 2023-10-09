from construct_base import ConstructBase
from str_construct_exceptions import StrConstructParseError

class StrConst(ConstructBase):
    def __init__(self, const, name=None):
        self.name = name
        self._const = const

    def _build(self, value):
        if value is not None and value != self._const:
            raise ValueError("StrConst needs the same constant value or nothing to build")

        return self._const

    def _parse(self, string):
        if string != self._const:
            raise StrConstructParseError(
                f"Received string ({string}) does not match the constant value ({self._const})"
            )
        return string
