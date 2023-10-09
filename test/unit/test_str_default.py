import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from str_int import StrInt
from str_default import StrDefault

class TestStrDefault:
    def test_build_with_value(self):
        assert StrDefault(StrInt("02X"), 17).build(2) == "02"

    def test_build_without_value(self):
        assert StrDefault(StrInt("02X"), 17).build() == "11"

    def test_parse_with_value(self):
        assert StrDefault(StrInt("02x"), 17).parse("10") == 16