import pytest

from strconstruct import StrCheck, StrCheckError, StrStruct, StrInt, StrRebuild, StrConst


class TestStrCheck:
    def test_condition_type(self):
        with pytest.raises(TypeError):
            StrCheck(2)
        with pytest.raises(TypeError):
            StrCheck("Hi")
        with pytest.raises(TypeError):
            StrCheck(None)
        with pytest.raises(TypeError):
            StrCheck(True)

    def test_build(self):
        d = StrCheck(lambda ctx: ctx["n"] > 2)
        assert d.build({}, n=3) == ""
        with pytest.raises(StrCheckError):
            d.build({}, n=2)

    def test_parse(self):
        d = StrCheck(lambda ctx: ctx["n"] > 2)
        assert d.parse("", n=3) == None
        with pytest.raises(StrCheckError):
            d.parse("", n=2)

    def test_struct(self):
        d = StrStruct(
            "f1" / StrInt("d"),
            StrCheck(lambda x: x["f1"] == 30)
        )
        assert d.build({"f1": 30}) == "30"
        assert d.parse("30") == {"f1": 30}
        with pytest.raises(StrCheckError):
            d.build({"f1": 31})
        with pytest.raises(StrCheckError):
            d.parse("31")

        d = StrStruct(
            "f1" / StrInt("d"),
            StrConst(","),
            "f2" / StrRebuild(StrInt("d"), lambda x: x["f1"] * 2),
            StrCheck(lambda x: x["f2"] == 30),
        )
        assert d.build({"f1": 15}) == "15,30"
        assert d.parse("15,30") == {"f1": 15, "f2": 30}

        with pytest.raises(StrCheckError):
            d.build({"f1": 14})
        with pytest.raises(StrCheckError):
            d.parse("14,31")
