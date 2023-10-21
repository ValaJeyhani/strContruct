import pytest

from strconstruct import StrInt, StrFloat, StrStruct, StrConst, StrDefault, StrConstructParseError


class TestStrStruct:
    def test_field_type(self):
        # TypeError: All items need to be of type ConstructBase
        with pytest.raises(TypeError):
            StrStruct("")

        StrStruct(
            "field1" / StrInt("d"),
            separator=",",
        )

    def test_build_type(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            separator=",",
        )
        # TypeError: The value for building an StrConstruct should be a dict
        with pytest.raises(TypeError):
            packet.build(2)

    def test_build_simple(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrInt("02X"),
            "field3" / StrFloat(".2f"),
        )
        output = packet.build(
            {
                "field1": 2,
                "field2": 15,
                "field3": 3.1,

            }
        )
        assert output == "20F3.10"
        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrInt("02X"),
            "field3" / StrFloat(".2f"),
            separator=":"
        )
        output = packet.build(
            {
                "field1": 2,
                "field2": 15,
                "field3": 3.1,

            }
        )
        assert output == "2:0F:3.10"

    def test_build_empty(self):
        packet = StrStruct(separator=",")
        assert packet.build({}) == ""
        packet = StrStruct()
        assert packet.build({}) == ""

    def test_build_with_nameless_fields(self):
        packet = StrStruct(
            StrConst(">>"),
            StrDefault(StrFloat("0.3f"), 2.345),
            "field2" / StrInt("02X"),
            separator=",",
        )
        output = packet.build(
            {
                "field2": 15,
            }
        )
        assert output == ">>,2.345,0F"

        packet = StrStruct(
            StrConst(">>"),
            StrDefault(StrFloat("0.3f"), 2.345),
            "field2" / StrInt("02X"),
        )
        output = packet.build(
            {
                "field2": 15,
            }
        )
        assert output == ">>2.3450F"

    def test_parse_simple(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrInt("02x"),
            "field3" / StrFloat(".2f"),
            separator=",",
        )
        assert  packet.parse("2,0f,3.10") == {
            "field1": 2,
            "field2": 15,
            "field3": 3.1,
        }

    def test_parse_no_separator(self):
        packet = StrStruct(
            "field1" / StrInt("1d"),
            "field2" / StrInt("02x"),
            "field3" / StrFloat(".2f"),
            "field4" / StrConst("@"),
            "field5" / StrFloat(".2f"),
        )
        assert  packet.parse("20f13.11@5.67") == {
            "field1": 2,
            "field2": 15,
            "field3": 13.11,
            "field4": "@",
            "field5": 5.67
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
            "field1" / StrInt("d"),
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
            "field1" / StrInt("d"),
            "field2" / StrInt("02X"),
            "field3" / StrStruct(
                "field4" / StrFloat(".2f"),
                "field5" / StrStruct(
                    "field6" / StrInt("03X"),
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
