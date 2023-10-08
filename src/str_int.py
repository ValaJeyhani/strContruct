from parse import parse

from construct_base import ConstructBase

class StrInt(ConstructBase):
    def _build(self, value):
        return f"{self._format}".format(value)

    def _parse(self, string):
        format_= self._format
        if format_ == "{:}":
            format_ = "{:d}"
        return parse(f"{format_}", string, case_sensitive=True)[0]
