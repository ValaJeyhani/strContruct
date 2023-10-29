import pytest

from strconstruct import StrStopIf, StrStruct, StrInt, StrFloat, StrConst, StrStopFieldError

class TestStrStopIf:
    def test_condition_type(self):
        with pytest.raises(TypeError):
            StrStopIf(2)
        with pytest.raises(TypeError):
            StrStopIf("Hi")
        with pytest.raises(TypeError):
            StrStopIf(None)

    def test_build_bool_condition(self):
        d = StrStopIf(True)
        with pytest.raises(StrStopFieldError):
            d.build({})
        d = StrStopIf(False)
        d.build({})

    def test_parse_bool_condition(self):
        d = StrStopIf(True)
        with pytest.raises(StrStopFieldError):
            d.parse("")
        d = StrStopIf(False)
        d.parse("")

    def test_build_lambda(self):
        d = StrStopIf(lambda this: this["n"])
        with pytest.raises(StrStopFieldError):
            d.build({}, n=True)
        d.build({}, n=False)

    def test_parse_lambda(self):
        d = StrStopIf(lambda this: this["n"])
        with pytest.raises(StrStopFieldError):
            d.parse({}, n=True)
        d.parse({}, n=False)

    def test_build_struct(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            StrStopIf(lambda this: this["n"]),
            StrConst(","),
            "field2" / StrFloat(".2f"),
        )
        assert packet.build({"field1": 2}, n=True) == "2"
        assert packet.build({"field1": 2, "field2": 3.1}, n=True) == "2"
        assert packet.build({"field1": 2, "field2": 3.1}, n=False) == "2,3.10"

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field_stop" / StrStopIf(lambda this: this["n"]),
            StrConst(","),
            "field2" / StrFloat(".2f"),
        )
        assert packet.build({"field1": 2}, n=True) == "2"
        assert packet.build({"field1": 2, "field2": 3.1}, n=True) == "2"
        assert packet.build({"field1": 2, "field2": 3.1}, n=False) == "2,3.10"
        # Even if there is a value with the same name of the StrStopIf field, it should be
        # able to ignore it and move on
        assert packet.build({"field1": 2, "field_stop": 2}, n=True) == "2"

        packet = StrStruct(
            "field1" / StrInt("d"),
            "_field_stop" / StrStopIf(lambda this: this["n"]),
            StrConst(","),
            "field2" / StrFloat(".2f"),
        )
        assert packet.build({"field1": 2}, n=True) == "2"
        assert packet.build({"field1": 2, "field2": 3.1}, n=False) == "2,3.10"

    def test_parse_struct(self):
        packet = StrStruct(
            "field1" / StrInt("d"),
            StrStopIf(lambda this: this["n"]),
            StrConst(","),
            "field2" / StrFloat(".2f"),
        )
        assert packet.parse("2", n=True) == {"field1": 2}
        assert packet.parse("2,3.10", n=True) == {"field1": 2}
        assert packet.parse("2,3.10", n=False) == {"field1": 2, "field2": 3.10}

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field_stop" / StrStopIf(lambda this: this["n"]),
            StrConst(","),
            "field2" / StrFloat(".2f"),
        )
        assert packet.parse("2", n=True) == {"field1": 2}
        assert packet.parse("2,3.10", n=True) == {"field1": 2}
        assert packet.parse("2,3.10", n=False) == {"field1": 2, "field2": 3.10}

        packet = StrStruct(
            "field1" / StrInt("d"),
            "field_stop" / StrStopIf(lambda this: this["n"]),
            StrConst(","),
            "field2" / StrFloat(".2f"),
        )
        assert packet.parse("2", n=True) == {"field1": 2}
