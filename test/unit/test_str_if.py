import pytest

from strconstruct import StrIf, StrInt, StrFloat, StrStruct, StrConst


class TestStrIf:
    def test_condition_type(self):
        with pytest.raises(TypeError):
            StrIf(2)
        with pytest.raises(TypeError):
            StrIf("Hi")
        with pytest.raises(TypeError):
            StrIf(None)

    def test_build_bool_condition(self):
        d = StrIf(True, StrInt("d"))
        assert d.build(2) == "2"
        d = StrIf(False, StrInt("d"))
        assert d.build(2) == ""

    def test_parse_bool_condition(self):
        d = StrIf(True, StrInt("d"))
        assert d.parse("2") == 2
        d = StrIf(False, StrInt("d"))
        assert d.parse("2") is None

    def test_build_lambda(self):
        d = StrIf(lambda this: this["n"], StrInt("d"))
        assert d.build(3, n=True) == "3"
        assert d.build(3, n=False) == ""

    def test_parse_lambda(self):
        d = StrIf(lambda this: this["n"], StrFloat(".2f"))
        assert d.parse(".23", n=True) == 0.23
        assert d.parse(".23", n=False) is None

    def test_build_struct(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            StrConst(","),
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
        )
        assert packet.build({"field1": 2, "field2": 2.34}, n=True) == "2,2.34"
        assert packet.build({"field1": 2, "field2": 2.34}, n=False) == "2,"

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            separator=","
        )
        assert packet.build({"field1": 2, "field2": 2.34}, n=True) == "2,2.34"
        assert packet.build({"field1": 2, "field2": 2.34}, n=False) == "2"

        packet = StrStruct(
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            StrConst(","),
            "field1" / StrInt("d"),
        )
        assert packet.build({"field1": 2, "field2": 2.34}, n=True) == "2.34,2"
        assert packet.build({"field1": 2, "field2": 2.34}, n=False) == ",2"

        packet = StrStruct(
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            "field1" / StrInt("d"),
            "field0" / StrInt("d"),
            separator=","
        )
        assert packet.build({"field0": 56, "field1": 2, "field2": 2.34}, n=True) == "2.34,2,56"
        assert packet.build({"field0": 56, "field1": 2, "field2": 2.34}, n=False) == "2,56"

    def test_parse_struct(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            StrConst(","),
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
        )
        assert packet.parse("2,2.34", n=True) == {"field1": 2, "field2": 2.34}
        assert packet.parse("2,2.34", n=False) == {"field1": 2}

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            separator=","
        )
        assert packet.parse("2,2.34", n=True) == {"field1": 2, "field2": 2.34}
        assert packet.parse("2,2.34", n=False) == {"field1": 2}

        packet = StrStruct(
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            StrConst(","),
            "field1" / StrInt("d"),
        )
        assert packet.parse("2.34,2", n=True) == {"field1": 2, "field2": 2.34}
        assert packet.parse(",2", n=False) == {"field1": 2}

        packet = StrStruct(
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            "field1" / StrInt("d"),
            "field0" / StrInt("d"),
            separator=","
        )
        assert packet.parse("2.34,2,3", n=True) == {"field0": 3, "field1": 2, "field2": 2.34}
        assert packet.parse("2,3", n=False) == {"field0": 3, "field1": 2}

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrIf(lambda this: this["n"], StrFloat(".2f")),
            separator=","
        )
        assert packet.parse("2,2.34", n=True) == {"field1": 2, "field2": 2.34}
        assert packet.parse("2", n=False) == {"field1": 2}
