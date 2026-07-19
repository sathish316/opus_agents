import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: end-to-end tests using pydantic_ai TestModel agents",
    )
