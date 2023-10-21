import pytest

from strconstruct import StrFloat, StrConstructParseError

class TestStrFloat:
#     def test_build_no_decimal(self):
#         assert StrFloat(".0f").build(2) == "2"
#         assert StrFloat(".0f").build(2.123) == "2"

    def test_parse_no_decimal_format(self):
        # assert StrFloat(".0f").parse("2") == 2
        # assert StrFloat(".f").parse("2.") == 2
        assert StrFloat(".f").parse(".2") == .2
        # assert StrFloat(".1f").parse("1.2@3.4") == 1.2
        assert isinstance(StrFloat("f").parse("2"), float)
        assert StrFloat(".0f").build(2.123) == "2"

    def test_build_one_decimal(self):
        assert StrFloat(".1f").build(2) == "2.0"
        assert StrFloat(".1f").build(2.0) == "2.0"
        assert StrFloat(".1f").build(2.0182374) == "2.0"
        assert StrFloat(".1f").build(2.0989898) == "2.1"
        assert StrFloat(".1f").build(12345.0989898) == "12345.1"
        assert StrFloat(".1f").parse("1.2@3.4") == 1.2
        assert StrFloat(".1f").parse(".2") == .2

    def test_parse_one_decimal(self):
        assert StrFloat(".1f").parse("2.1") == 2.1
        assert StrFloat(".1f").parse("2.0") == 2

    def test_parse_one_decimal_fails_with_less_decimals_input(self):
        with pytest.raises(StrConstructParseError):
            StrFloat(".4f").parse("2.018")
        with pytest.raises(StrConstructParseError):
            StrFloat(".10f").parse("2.111111111")
        assert StrFloat(".10f").parse("2.1111111111") == 2.1111111111

    def test_build_six_decimal(self):
        assert StrFloat(".6f").build(2) == "2.000000"
        assert StrFloat(".6f").build(2.0000001) == "2.000000"
        assert StrFloat(".6f").build(2.0000009) == "2.000001"

    def test_parse_two_digit_format(self):
        assert StrFloat(".10f").parse("2.1234567891") == 2.1234567891

    def test_parse_consumes_as_many_chars_as_specified_in_format(self):
        assert StrFloat(".1f").parse("2.1b") == 2.1
        assert StrFloat(".2f").parse("2.12W") == 2.12
        assert StrFloat(".2f").parse("2.20Foo") == 2.20
        assert StrFloat(".6f").parse("2.0000001") == 2.000000
        assert StrFloat(".6f").parse("2.0000009") == 2.000000

    def test_parse_consumes_greedily(self):
        assert StrFloat("f").parse("19.98765@") == 19.98765
        assert StrFloat("f").parse("19") == 19
        assert StrFloat("f").parse("19.1@") == 19.1
