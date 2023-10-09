from construct_base import ConstructBase

class StrDefault(ConstructBase):
    def __init__(self, construct, default, name=None, format_processed=False):
        self._subconstruct = construct
        self._default = default
        self.name = name

    def _build(self, value):
        if value is None:
            return self._subconstruct.build(self._default)

        return self._subconstruct.build(value)

    def _parse(self, string):
        return self._subconstruct.parse(string)
