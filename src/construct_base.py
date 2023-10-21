from .str_construct_exceptions import StrConstructBuildError


class ConstructBase:
    def __init__(self, format_):
        self._format = f"{{:{format_}}}"
        self.name = None
        self._parse_left = None

    def _div(self, other):
        if not isinstance(other, str):
            raise TypeError("Division is support only for strings")
        self.name = other
        return self

    def __truediv__(self, other):
        return self._div(other)

    def __rtruediv__(self, other):
        return self._div(other)

    def _build(self, value, **kwargs):
        raise NotImplementedError("Should be overridden by the child classes")

    def _parse(self, string, **kwargs):
        raise NotImplementedError("Should be overridden by the child classes")

    def build(self, value=None, **kwargs):
        # Some StrConstruct class do not necessarily need a value for building. StrConst
        # and StrDefault are sample examples.
        return self._build(value, **kwargs)

    def parse(self, string, **kwargs):
        return self._parse(string, **kwargs)

    def parse_left(self):
        if self._parse_left is None:
            raise RuntimeError("No parse has been requested or the last one failed")
        output = self._parse_left
        self._parse_left = None
        return output
