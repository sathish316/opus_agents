import logging
from datetime import datetime, timedelta
from typing import Tuple

logger = logging.getLogger(__name__)

class DatetimeHelper:
    """Helper class for datetime operations"""

    def __init__(self):
        pass

    def get_last_week_daterange(self) -> Tuple[str, str]:
        """Get the date range for the last week"""
        logger.info("Getting date range for last week")
        now = datetime.now()
        weekday = now.weekday()  # Monday is 0, Sunday is 6

        # Get Monday of current week
        current_monday = now - timedelta(days=weekday)

        # Go back 7 days to get Monday of last week
        last_monday = current_monday - timedelta(days=7)
        last_sunday = last_monday + timedelta(days=6)
        # Add one day to include tasks completed on Sunday
        next_monday = last_sunday + timedelta(days=1)

        since = last_monday.strftime("%Y-%m-%d")
        until = next_monday.strftime("%Y-%m-%d")
        return since, until

    def get_current_week_daterange(self) -> Tuple[str, str]:
        """Get the date range for the current week"""
        logger.info("Getting date range for current week")
        now = datetime.now()
        weekday = now.weekday()  # Monday is 0, Sunday is 6

        monday = now - timedelta(days=weekday)
        sunday = monday + timedelta(days=6)
        # Add one day to include tasks completed on Sunday
        next_monday = sunday + timedelta(days=1)

        since = monday.strftime("%Y-%m-%d")
        until = next_monday.strftime("%Y-%m-%d")

        return since, until

    def get_today_daterange(self) -> Tuple[str, str]:
        """Get start/end date for today"""
        logger.info("Getting date range for today")
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        return today, tomorrow

    def get_yesterday_daterange(self) -> Tuple[str, str]:
        """Get start/end date for yesterday"""
        logger.info("Getting date range for yesterday")
        now = datetime.now()
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        today = now.strftime("%Y-%m-%d")
        return yesterday, today

    def get_last_week_datetime_range(self) -> Tuple[str, str]:
        """Get the date range for the last week"""
        logger.info("Getting datetime range for last week")
        now = datetime.now()
        weekday = now.weekday()  # Monday is 0, Sunday is 6

        # Get Monday of current week
        current_monday = now - timedelta(days=weekday)

        # Go back 7 days to get Monday of last week
        last_monday = current_monday - timedelta(days=7)
        last_sunday = last_monday + timedelta(days=6)
        # Add one day to include tasks completed on Sunday
        next_monday = last_sunday + timedelta(days=1)

        since = last_monday.strftime("%Y-%m-%dT00:00:00Z")
        until = next_monday.strftime("%Y-%m-%dT00:00:00Z")
        return since, until

    def get_current_week_datetime_range(self) -> Tuple[str, str]:
        """Get the date range for the current week"""
        logger.info("Getting datetime range for current week")
        now = datetime.now()
        weekday = now.weekday()  # Monday is 0, Sunday is 6

        monday = now - timedelta(days=weekday)
        sunday = monday + timedelta(days=6)
        # Add one day to include tasks completed on Sunday
        next_monday = sunday + timedelta(days=1)

        since = monday.strftime("%Y-%m-%dT00:00:00Z")
        until = next_monday.strftime("%Y-%m-%dT00:00:00Z")

        return since, until

    def get_next_week_datetime_range(self) -> Tuple[str, str]:
        """Get the date range for the next week"""
        logger.info("Getting datetime range for next week")
        now = datetime.now()
        weekday = now.weekday()  # Monday is 0, Sunday is 6

        monday = now - timedelta(days=weekday)
        sunday = monday + timedelta(days=6)
        # Add one day to include tasks completed on Sunday
        next_monday = sunday + timedelta(days=1)

        since = next_monday.strftime("%Y-%m-%dT00:00:00Z")
        until = (next_monday + timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")

        return since, until

    def get_today_datetime_range(self) -> Tuple[str, str]:
        """Get start/end date for today"""
        logger.info("Getting datetime range for today")
        now = datetime.now()
        today = now.strftime("%Y-%m-%dT00:00:00Z")
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        return today, tomorrow

    def get_yesterday_datetime_range(self) -> Tuple[str, str]:
        """Get start/end date for yesterday"""
        logger.info("Getting datetime range for yesterday")
        now = datetime.now()
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        today = now.strftime("%Y-%m-%dT00:00:00Z")
        return yesterday, today

    def get_tomorrow_datetime_range(self) -> Tuple[str, str]:
        """Get start/end date for tomorrow"""
        logger.info("Getting datetime range for tomorrow")
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        day_after_tomorrow = (now + timedelta(days=2)).strftime("%Y-%m-%dT00:00:00Z")
        return tomorrow, day_after_tomorrow

    def get_next_date(self, date: str, days: int = 1) -> str:
        """Get the next date"""
        return (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=days)).strftime(
            "%Y-%m-%d"
        )

    def get_next_datetime(self, date: str, days: int = 1) -> str:
        """Get the next date"""
        return (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=days)).strftime(
            "%Y-%m-%dT00:00:00Z"
        )

    def format_datetime(self, date: str) -> str:
        """Format datetime"""
        # Check if date is in yyyy-MM-dd format and reformat to datetime format
        if len(date) == 10 and date.count('-') == 2:
            # Convert yyyy-MM-dd to yyyy-MM-ddT00:00:00Z
            date = date + "T00:00:00Z"
        return date
