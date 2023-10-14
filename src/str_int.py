from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructParseError

class StrInt(ConstructBase):
    def __init__(self, format_):
        self.name = None
        self._format = f"{{:{format_}}}"

        if len(format_) == 0:
            raise ValueError(
                "Invalid format. At least the integer representation should be "
                "provided (e.g. 'd', 'x' etc.)"
            )

        self._format_type = format_[-1]
        if self._format_type not in ["d", "x", "X"]:
            raise ValueError(f"Format ({self._format_type}) not supported by StrInt")

        self._supported_chars = [str(item) for item in range(10)]
        if self._format_type == "x":
            self._supported_chars += [chr(item) for item in range(ord("a"), ord("f") + 1)]
        elif self._format_type == "X":
            self._supported_chars += [chr(item) for item in range(ord("A"), ord("F") + 1)]

        if format_[0] == "0":
            _format_length = format_[1:-1]
        else:
            _format_length = format_[0:-1]
        try:
            self._format_length = int(_format_length)
        except ValueError:
            self._format_length = None

    def _build(self, value):
        return f"{self._format}".format(value)

    def _parse(self, string):
        if string[0] == "-":
            multiplier = -1
            string = string[1:]
        elif string[0] == "+":
            multiplier = 1
            string = string[1:]
        else:
            multiplier = 1
        if self._format_length is not None:
            if len(string) < self._format_length:
                raise StrConstructParseError(
                    f"Insufficient characters found. At least {self._format_length} "
                    "character is needed"
                )
            number = string[:self._format_length]
            parse_left = string[self._format_length:]
        else:
            number = []
            for index, char in enumerate(string):
                if char in self._supported_chars:
                    number.append(char)
                else:
                    break
            number = "".join(number)
            parse_left = string[index:]

        if number == "":
            raise StrConstructParseError("No numeric content collected from the input")

        self._parse_left = parse_left
        if self._format_type == "d":
            return int(number) * multiplier
        if self._format_type == "x" or self._format_type == "X":
            return int(number, 16) * multiplier
