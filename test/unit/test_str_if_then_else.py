import pytest

from strconstruct import StrIfThenElse, StrInt, StrFloat, StrStruct, StrConst


class TestStrIfThenElse:
    def test_condition_type(self):
        with pytest.raises(TypeError):
            StrIfThenElse(2)
        with pytest.raises(TypeError):
            StrIfThenElse("Hi")
        with pytest.raises(TypeError):
            StrIfThenElse(None)

    def test_build_bool_condition(self):
        d = StrIfThenElse(True, StrInt("d"), StrFloat(".2f"))
        assert d.build(2) == "2"
        d = StrIfThenElse(False, StrInt("d"), StrFloat(".2f"))
        assert d.build(2) == "2.00"

    def test_parse_bool_condition(self):
        d = StrIfThenElse(True, StrInt("d"), StrFloat(".2f"))
        assert d.parse("2.00") == 2
        d = StrIfThenElse(False, StrInt("d"), StrFloat(".2f"))
        assert d.parse("2.00") == 2.00

    def test_build_lambda(self):
        d = StrIfThenElse(lambda this: this["n"], StrInt("d"), StrFloat(".2f"))
        assert d.build(3, n=True) == "3"
        assert d.build(3, n=False) == "3.00"

    def test_parse_lambda(self):
        d = StrIfThenElse(lambda this: this["n"], StrInt("d"), StrFloat(".2f"))
        assert d.parse("1.23", n=True) == 1
        assert d.parse("1.23", n=False) == 1.23

    def test_build_struct(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            StrConst(","),
            "field2" / StrIfThenElse(lambda this: this["field1"] > 2, StrFloat(".3f"), StrFloat(".2f")),
        )
        assert packet.build({"field1": 2, "field2": 2.343}) == "2,2.34"
        assert packet.build({"field1": 3, "field2": 2.343}) == "3,2.343"

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrIfThenElse(lambda this: this["n"], StrFloat(".2f"), StrFloat(".3f")),
            separator=","
        )
        assert packet.build({"field1": 2, "field2": 2.343}, n=True) == "2,2.34"
        assert packet.build({"field1": 2, "field2": 2.343}, n=False) == "2,2.343"

        packet = StrStruct(
            "field2" / StrIfThenElse(lambda this: this["n"], StrFloat(".2f"), StrFloat(".3f")),
            StrConst(","),
            "field1" / StrInt("d"),
        )
        assert packet.build({"field1": 2, "field2": 2.343}, n=True) == "2.34,2"
        assert packet.build({"field1": 2, "field2": 2.343}, n=False) == "2.343,2"

        packet = StrStruct(
            "field2" / StrIfThenElse(lambda this: this["n"], StrFloat(".2f"), StrFloat(".3f")),
            "field1" / StrInt("d"),
            "field0" / StrInt("d"),
            separator=","
        )
        assert packet.build({"field0": 5, "field1": 2, "field2": 2.343}, n=True) == "2.34,2,5"
        assert packet.build({"field0": 5, "field1": 2, "field2": 2.343}, n=False) == "2.343,2,5"

    def test_parse_struct(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            StrConst(","),
            "field2" / StrIfThenElse(lambda this: this["field1"] > 2, StrFloat(".3f"), StrFloat(".2f")),
        )
        assert packet.parse("2,2.343") == {"field1": 2, "field2": 2.34}
        assert packet.parse("3,2.343") == {"field1": 3, "field2": 2.343}

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field2" / StrIfThenElse(lambda this: this["field1"] > 2, StrFloat(".3f"), StrFloat(".2f")),
            separator=","
        )
        assert packet.parse("2,2.343") == {"field1": 2, "field2": 2.34}
        assert packet.parse("3,2.343") == {"field1": 3, "field2": 2.343}
