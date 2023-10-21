from .construct_base import ConstructBase

class StrDefault(ConstructBase):
    def __init__(self, construct, default):
        self._subconstruct = construct
        self._default = default
        self.name = None

    def _build(self, value, **kwargs):
        # TODO: This should work with empty dict instead of None. See the following link
        # https://construct.readthedocs.io/en/latest/misc.html#default
        if value is None:
            return self._subconstruct.build(self._default)

        return self._subconstruct.build(value)

    def _parse(self, string, **kwargs):
        return self._subconstruct.parse(string)
