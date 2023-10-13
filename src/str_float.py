from construct_base import ConstructBase
from str_construct_exceptions import StrConstructParseError

class StrFloat(ConstructBase):
    def __init__(self, format_):
        self.name = None
        self._format = f"{{:{format_}}}"

        if len(format_) == 0:
            raise ValueError("Invalid format. Only 'f' is supported by StrFloat")

        self._format_type = format_[-1]
        if self._format_type != "f":
            raise ValueError(f"Format ({self._format_type}) not supported by StrFloat")

        break_down = format_[:-1].split(".")
        try:
            self._format_length = int(break_down[1])
        # ValueError happens if breakdown[1] is an empty string
        # IndexError happens if there is not index 1 at all
        except (ValueError, IndexError):
            self._format_length = 0

    def _build(self, value):
        return f"{self._format}".format(value)

    def _parse(self, string):
        break_down = string.split(".")
        if len(break_down) == 1:
            whole = break_down[0]
            decimal = ""
        else:
            whole, decimal = break_down[0:2]
        if len(decimal) < self._format_length:
            raise StrConstructParseError(
                f"Insufficient characters found. At least {self._format_length} "
                "decimal numbers are needed"
            )
        self._parse_left = string[(len(whole) + 1 + self._format_length):]
        return float(".".join([whole, decimal[:self._format_length]]))
