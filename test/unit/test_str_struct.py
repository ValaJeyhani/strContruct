import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from str_int import StrInt
from str_float import StrFloat
from str_struct import StrStruct
from str_const import StrConst
from str_construct_exceptions import StrConstructParseError

class TestStrStruct:
    def test_field_type(self):
        with pytest.raises(TypeError):
            StrStruct("")

        StrStruct(
            "field1" / StrInt(""),
            separator=",",
        )

    def test_build_type(self):
        packet = StrStruct(
            "field1" / StrInt(""),
            separator=",",
        )
        with pytest.raises(TypeError):
            packet.build(2)

    def test_build_simple(self):
        packet = StrStruct(
            "field1" / StrInt(""),
            "field2" / StrInt("02X"),
            "field3" / StrFloat(".2f"),
            separator=",",
        )
        output = packet.build(
            {
                "field1": 2,
                "field2": 15,
                "field3": 3.1,

            }
        )
        assert output == "2,0F,3.10"

    def test_build_empty(self):
        packet = StrStruct(
            separator=",",
        )
        output = packet.build({})
        assert output == ""

    def test_build_with_nameless_fields(self):
        packet = StrStruct(
            StrConst(">>"),
            "field2" / StrInt("02X"),
            separator=",",
        )
        output = packet.build(
            {
                "field2": 15,
            }
        )
        assert output == ">>,0F"

    def test_parse_simple(self):
        packet = StrStruct(
            "field1" / StrInt(""),
            "field2" / StrInt("02x"),
            "field3" / StrFloat(".2f"),
            separator=",",
        )
        output = packet.parse("2,0f,3.10")
        assert output == {
                "field1": 2,
                "field2": 15,
                "field3": 3.1,

            }

    def test_parse_with_nameless_fields(self):
        packet = StrStruct(
            StrConst("@>"),
            "field2" / StrInt("03x"),
            separator=",",
        )
        output = packet.parse("@>,00a")
        assert output == {"field2": 10}
        with pytest.raises(StrConstructParseError):
            packet.parse("00a")
        with pytest.raises(StrConstructParseError):
            packet.parse(",00a")
        with pytest.raises(StrConstructParseError):
            packet.parse(">,00a")
        with pytest.raises(StrConstructParseError):
            packet.parse("@,00a")

    def test_parse_with_underscored_fields(self):
        packet = StrStruct(
            StrConst("@>"),
            "_field2" / StrInt("03x"),
            "_field3" / StrInt("02x"),
            separator=",",
        )
        output = packet.parse("@>,00a,0f")
        assert output == {}
        with pytest.raises(StrConstructParseError):
            packet.parse("")

    def test_build_nested(self):
        packet = StrStruct(
            "field1" / StrInt(""),
            "field2" / StrInt("02X"),
            "field3" / StrStruct(
                "field4" / StrFloat(".2f"),
                separator=",",
            ),
            separator=",",
        )
        output = packet.build(
            {
                "field1": 2,
                "field2": 15,
                "field3": {
                    "field4": 3.1,
                }

            }
        )
        assert output == "2,0F,3.10"

        packet = StrStruct(
            "field1" / StrInt(""),
            "field2" / StrInt("02X"),
            "field3" / StrStruct(
                "field4" / StrFloat(".2f"),
                "field5" / StrStruct(
                    "field6" / StrFloat("03X"),
                    separator=",",
                ),
                separator=",",
            ),
            separator=",",
        )
        output = packet.build(
            {
                "field1": 2,
                "field2": 15,
                "field3": {
                    "field4": 3.1,
                    "field5": {
                        "field6": 10,
                    }
                }

            }
        )
        assert output == "2,0F,3.10,00A"