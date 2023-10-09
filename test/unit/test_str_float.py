import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from str_float import StrFloat
from str_construct_exceptions import StrConstructMismatchingFormatError

class TestStrFloat:
    def test_build_no_decimal(self):
        assert StrFloat(".0f").build(2) == "2"
        assert StrFloat(".0f").build(2.123) == "2"

    def test_parse_no_decimal(self):
        assert StrFloat(".0f").parse("2") == 2
        assert isinstance(StrFloat("f").parse("2"), float)
        assert StrFloat(".0f").build(2.123) == "2"

    def test_build_one_decimal(self):
        assert StrFloat(".1f").build(2) == "2.0"
        assert StrFloat(".1f").build(2.0) == "2.0"
        assert StrFloat(".1f").build(2.0182374) == "2.0"
        assert StrFloat(".1f").build(2.0989898) == "2.1"

    def test_parse_one_decimal(self):
        assert StrFloat(".1f").parse("2.1") == 2.1
        assert StrFloat(".1f").parse("2.0") == 2

    @pytest.mark.xfail()
    def test_parse_one_decimal_fails_with_more_decimals_input(self):
        with pytest.raises(StrConstructMismatchingFormatError):
            StrFloat(".1f").parse("2.0182374")
        with pytest.raises(StrConstructMismatchingFormatError):
            StrFloat(".1f").parse("2.0989898")

    def test_build_six_decimal(self):
        assert StrFloat(".6f").build(2) == "2.000000"
        assert StrFloat(".6f").build(2.0000001) == "2.000000"
        assert StrFloat(".6f").build(2.0000009) == "2.000001"

    @pytest.mark.xfail()
    def test_parse_six_decimal(self):
        assert StrFloat(".6f").parse("2.000000") == 2
        assert StrFloat(".6f").parse("2.0000001") == 2.000000
        assert StrFloat(".6f").parse("2.0000009") == 2.000001
