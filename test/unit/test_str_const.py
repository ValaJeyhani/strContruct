import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from str_const import StrConst
from str_construct_exceptions import StrConstructParseError

class TestStrStruct:
    def test_build_fails_with_value(self):
        packet = StrConst("MyString")
        with pytest.raises(ValueError):
            packet.build(2)
        packet.build("MyString")

    def test_build(self):
        packet = StrConst(">@")
        assert packet.build() == ">@"

    def test_parse(self):
        packet = StrConst(">@")
        assert packet.parse(">@") == ">@"

    def test_parse_not_match_fails(self):
        packet = StrConst(">@")
        with pytest.raises(StrConstructParseError):
            assert packet.parse("@") == ">@"