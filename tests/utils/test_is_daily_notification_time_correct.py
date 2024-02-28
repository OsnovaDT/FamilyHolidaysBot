"""Tests for is_daily_notification_time_correct function"""

from pytest import mark

from tests.constants import NOT_STR_VALUES
from tests.mocks import NOTIFICATION_TIME_AND_IS_CORRECT
from utils import is_daily_notification_time_correct


@mark.asyncio
@mark.parametrize(
    "time_,expected_is_correct", NOTIFICATION_TIME_AND_IS_CORRECT
)
async def test_is_daily_notification_time_correct(
    time_, expected_is_correct
) -> None:
    """Test is_daily_notification_time_correct function"""

    real_is_correct = await is_daily_notification_time_correct(time_)
    assert real_is_correct is expected_is_correct, time_


@mark.asyncio
async def test_is_daily_notification_time_correct_with_wrong_params() -> None:
    """Test is_daily_notification_time_correct function with wrong params"""

    for value in NOT_STR_VALUES.values():
        real_is_correct = await is_daily_notification_time_correct(value)
        assert real_is_correct is False, value
