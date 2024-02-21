"""Tests for _get_age_suffix function"""

from pytest import mark

from tests.mocks import AGE_AND_SUFFIX, WRONG_AGES
from utils import _get_age_suffix


@mark.asyncio
@mark.parametrize("age,expected_suffix", AGE_AND_SUFFIX)
async def test__get_age_suffix_correct(age, expected_suffix) -> None:
    """Test _get_age_suffix function with correct data"""

    real_suffix = await _get_age_suffix(age)
    assert real_suffix == expected_suffix


@mark.asyncio
async def test__get_age_suffix_wrong() -> None:
    """Test _get_age_suffix function with wrong data"""

    for age in WRONG_AGES:
        real_suffix = await _get_age_suffix(age)
        assert real_suffix == ""
