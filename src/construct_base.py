class ConstructBase:
    def __init__(self, format_, name=None, format_processed=False):
        if format_processed is False:
            self._format = f"{{:{format_}}}"
        else:
            self._format = format_
        self.name = name

    def _div(self, other):
        if not isinstance(other, str):
            raise TypeError("Division is support only for strings")
        return self.__class__(self._format, other, format_processed=True)

    def __truediv__(self, other):
        return self._div(other)

    def __rtruediv__(self, other):
        return self._div(other)

    def _build(self, value):
        raise NotImplementedError("Should be overridden by the child classes")

    def _parse(self, string):
        raise NotImplementedError("Should be overridden by the child classes")

    def build(self, value):
        return self._build(value)

    def parse(self, string):
        return self._parse(string)

if __name__ == "__main__":
    m = ConstructBase("")
    m / "my_name"