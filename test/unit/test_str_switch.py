import pytest

from strconstruct import (
    StrSwitch, StrFloat, StrConst, StrInt, StrDefault, StrStruct, StrConstructBuildError,
    StrConstructParseError
)


class TestStrSwitch:
    def test_build_constant_condition(self):
        d = StrSwitch(
            1,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.build(2) == "2.0"

        d = StrSwitch(
            2,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.build() == "@"

        d = StrSwitch(
            3,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            },
            default=StrInt("d")
        )
        assert d.build(13) == "13"

        d = StrSwitch(
            3,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            },
        )
        with pytest.raises(StrConstructBuildError):
            d.build()

    def test_parse_constant_condition(self):
        d = StrSwitch(
            1,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.parse("2.0") == 2.0

        d = StrSwitch(
            2,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.parse("@") == "@"

        d = StrSwitch(
            3,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            },
            default=StrInt("d")
        )
        assert d.parse("13") == 13

        d = StrSwitch(
            3,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            },
        )
        with pytest.raises(StrConstructParseError):
            d.parse("")

    def test_build_callable_condition(self):
        d = StrSwitch(
            lambda ctx: 1,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.build(2) == "2.0"

        d = StrSwitch(
            lambda ctx: 2,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.build() == "@"

    def test_parse_callable_condition(self):
        d = StrSwitch(
            lambda ctx: 1,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.parse("2.0") == 2.

        d = StrSwitch(
            lambda ctx: 2,
            {
                1: StrFloat("0.1f"),
                2: StrConst("@")
            }
        )
        assert d.parse("@") == "@"

    def test_build_with_context(self):
        """See the following link for more examples from Construct itself

        https://construct.readthedocs.io/en/latest/misc.html?highlight=switch#switch
        """
        d = StrSwitch(
            lambda this: this["n"],
            {
                1: StrFloat("0.1f"),
                2: StrConst("@"),
                3: StrDefault(StrInt("03X"), 17),
                4: StrStruct(
                    "field1" / StrInt("d"),
                    StrConst("-"),
                    "field2" / StrFloat(".2f"),
                )
            },
            default=StrInt("d")
        )
        assert d.build(2, n=1) == "2.0"
        assert d.build(n=2) == "@"
        assert d.build(n=3) == "011"
        assert d.build(16, n=3) == "010"
        assert d.build(14, n=103) == "14"

        output = d.build(
            {
                "field1": 13,
                "field2": 17.29,
            },
            n=4,
        )
        assert output == "13-17.29"

    def test_parse_with_context(self):
        d = StrSwitch(
            lambda this: this["n"],
            {
                1: StrFloat("0.1f"),
                2: StrConst("@"),
                3: StrDefault(StrInt("03X"), 17),
                4: StrStruct(
                    "field1" / StrInt("d"),
                    StrConst("-"),
                    "field2" / StrFloat(".2f"),
                )
            },
            default=StrInt("d")
        )
        assert d.parse("0.2", n=1) == 0.2
        assert d.parse("@", n=2) == "@"
        assert d.parse("011", n=3) == 17
        assert d.parse("14", n=103) == 14

        output = d.parse("78-198.23", n=4)
        assert output == {
            "field1": 78,
            "field2": 198.23
        }
