from dataclasses import dataclass


@dataclass
class GCalMeeting:
    """Represents a meeting from Google Calendar"""
    summary: str
