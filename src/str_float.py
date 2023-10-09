from parse import parse

from construct_base import ConstructBase
from str_construct_exceptions import StrConstructParsingError

class StrFloat(ConstructBase):
    def _build(self, value):
        return f"{self._format}".format(value)

    def _parse(self, string):

        format_= self._format
        if format_ == "{:}":
            format_ = "{:f}"
        # A workaround for the parse module as its required format for floating-point
        # numbers is "g" rather than "f"
        format_ = format_.replace("f}", "g}")
        parsed = parse(f"{format_}", string, case_sensitive=True)
        if parsed is None:
            raise StrConstructParsingError(f"Could not parse \"{string}\" with format {self._format}")
        return parsed[0]
