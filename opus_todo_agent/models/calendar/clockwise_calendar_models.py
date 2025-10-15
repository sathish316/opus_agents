from dataclasses import dataclass


@dataclass
class ClockwiseMeeting:
    """Represents a meeting from Clockwise"""
    eventJson: dict
