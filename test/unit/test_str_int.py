import pytest

from strconstruct import StrInt, StrConstructParseError

class TestStrInt:
    def test_build_positive(self):
        assert StrInt("d").build(2) == "2"

    def test_parse_positive(self):
        assert StrInt("d").parse("2") == 2

    def test_build_negative(self):
        assert StrInt("d").build(-2) == "-2"

    def test_parse_negative(self):
        assert StrInt("d").parse("-2") == -2

    def test_build_hex_lower_case(self):
        assert StrInt("x").build(15) == "f"

    def test_parse_hex_lower_case(self):
        assert StrInt("x").parse("f") == 15

    def test_parse_hex_lower_case_raises_error(self):
        with pytest.raises(StrConstructParseError):
            StrInt("x").parse("F")

    def test_build_hex_padding(self):
        assert StrInt("03X").build(10) == "00A"
        assert StrInt("013X").build(10) == "000000000000A"

    def test_parse_hex_padding(self):
        assert StrInt("03X").parse("00A") == 10
        assert StrInt("013X").parse("000000000000A") == 10
        assert StrInt("13X").parse("000000000000A") == 10

    def test_parse_longer_input_than_format(self):
        assert StrInt("03X").parse("00A1394756") == 10
        assert StrInt("1X").parse("40A1394756") == 4
        assert StrInt("1d").parse("123") == 1
        assert StrInt("2d").parse("123") == 12
        assert StrInt("3d").parse("123") == 123

    def test_parse_shorter_input_than_format(self):
        with pytest.raises(StrConstructParseError) as info:
            StrInt("3d").parse("12")
            assert info.value.message.startswith("Insufficient characters found")
        with pytest.raises(StrConstructParseError) as info:
            StrInt("13X").parse("00000000000A")
            assert info.value.message.startswith("Insufficient characters found")
