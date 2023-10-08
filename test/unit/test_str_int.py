import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from str_int import StrInt
from str_construct_exceptions import StrConstructMismatchingFormatError

class TestStrInt:
    def test_build_positive(self):
        assert StrInt("").build(2) == "2"

    def test_parse_positive(self):
        assert StrInt("").parse("2") == 2

    def test_build_negative(self):
        assert StrInt("").build(-2) == "-2"

    def test_parse_negative(self):
        assert StrInt("").parse("-2") == -2

    def test_build_hex_lower_case(self):
        assert StrInt("x").build(15) == "f"

    def test_parse_hex_lower_case(self):
        assert StrInt("x").parse("f") == 15

    @pytest.mark.xfail()
    def test_parse_hex_lower_case_raises_error(self):
        with pytest.raises(StrConstructMismatchingFormatError):
            StrInt("x").parse("F")

    def test_build_hex_padding(self):
        assert StrInt("03X").build(10) == "00A"

    @pytest.mark.xfail()
    def test_parse_hex_padding(self):
        assert StrInt("03X").parse("00A") == 10