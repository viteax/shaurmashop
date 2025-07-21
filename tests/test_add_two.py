import pytest


def multiple_by_two(n):
    return n * 2


@pytest.mark.parametrize('test_input,expected', [(0, 0), (1, 2)])
def test_add_two(test_input, expected):
    res = multiple_by_two(test_input)

    assert res == expected
