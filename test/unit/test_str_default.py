import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from str_int import StrInt
from str_float import StrFloat
from str_default import StrDefault

class TestStrDefault:
    def test_build_with_value(self):
        assert StrDefault(StrInt("02X"), 17).build(2) == "02"
        assert StrDefault(StrFloat("0.3f"), 17.984).build(2) == "2.000"

    def test_build_without_value(self):
        assert StrDefault(StrInt("02X"), 17).build() == "11"
        assert StrDefault(StrFloat("0.3f"), 17.984).build() == "17.984"

    def test_parse_with_value(self):
        assert StrDefault(StrInt("02x"), 17).parse("10") == 16
        assert StrDefault(StrFloat(".3f"), 17.984).parse("11.123") == 11.123
