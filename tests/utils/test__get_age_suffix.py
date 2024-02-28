"""Tests for _get_age_suffix function"""

from pytest import mark

from tests.constants import WRONG_AGES
from tests.mocks import AGE_AND_SUFFIX
from utils import _get_age_suffix


@mark.asyncio
@mark.parametrize("age,expected_suffix", AGE_AND_SUFFIX)
async def test__get_age_suffix_correct(age, expected_suffix) -> None:
    """Test _get_age_suffix function with correct data"""

    real_suffix = await _get_age_suffix(age)
    assert real_suffix == expected_suffix, age


@mark.asyncio
async def test__get_age_suffix_with_wrong_params() -> None:
    """Test _get_age_suffix function with wrong params"""

    for age in WRONG_AGES.values():
        real_suffix = await _get_age_suffix(age)
        assert real_suffix == "", age
