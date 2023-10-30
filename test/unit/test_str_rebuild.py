import pytest

from strconstruct import StrRebuild, StrInt, StrStruct, StrConst, StrFloat, StrDefault


class TestStrRebuild:
    def test_callback_type(self):
        with pytest.raises(TypeError):
            StrRebuild(StrInt, 2)
        with pytest.raises(TypeError):
            StrRebuild(StrInt, "Hi")
        with pytest.raises(TypeError):
            StrRebuild(StrInt, None)

    def test_build(self):
        d = StrRebuild(StrInt("d"), lambda x: 2 * x["n"])
        assert d.build({}, n=2) == "4"
        assert d.build({"a": 3}, n=2) == "4"
        assert d.build({"n": 3}, n=2) == "4"  # _value_ is completely ignore by StrBuild

    def test_parse(self):
        d = StrRebuild(StrInt("d"), lambda x: 2 * x["n"])
        assert d.parse("23") == 23

    def test_build_struct(self):
        d = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrConst(":"),
            "field3" / StrRebuild(StrFloat(".1f"), lambda x: x["field1"] + 10)
        )
        assert d.build({"field1": 3}) == "3:13.0"

        d = StrStruct(
            "field1" / StrInt("d"),
            "field3" / StrRebuild(StrFloat(".1f"), lambda x: x["field1"] * 2.3),
            separator=",",
        )
        assert d.build({"field1": 5}) == "5,11.5"

        d = StrStruct(
            "stx" / StrDefault(StrInt("02X"), 12),
            "counter" / StrInt("d"),
            "payload" / StrInt("d"),
            "checksum" / StrRebuild(
                StrInt("d"),
                lambda this: this["stx"] + this["counter"] + this["payload"]
            ),
            "etx" / StrConst("\n"),
        )
        d.build({"counter": 3, "payload": 5})

    def test_parse_struct(self):
        d = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrConst(":"),
            "field3" / StrRebuild(StrFloat(".1f"), lambda x: x["field1"] + 10)
        )
        assert d.parse("3:13.0") == {"field1": 3, "field2": ":", "field3": 13.0}

        d = StrStruct(
            "field1" / StrInt("d"),
            "field3" / StrRebuild(StrFloat(".1f"), lambda x: x["field1"] * 2.3),
            separator=",",
        )
        assert d.parse("5,11.5") == {"field1": 5, "field3": 11.5}
