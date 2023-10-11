class ConstructBase:
    def __init__(self, format_):
        self._format = f"{{:{format_}}}"
        self.name = None

    def _div(self, other):
        if not isinstance(other, str):
            raise TypeError("Division is support only for strings")
        self.name = other
        return self

    def __truediv__(self, other):
        return self._div(other)

    def __rtruediv__(self, other):
        return self._div(other)

    def _build(self, value):
        raise NotImplementedError("Should be overridden by the child classes")

    def _parse(self, string):
        raise NotImplementedError("Should be overridden by the child classes")

    def build(self, value=None):
        # Some StrConstruct class do not necessarily need a value for building. StrConst
        # and StrDefault are sample examples.
        return self._build(value)

    def parse(self, string):
        return self._parse(string)
