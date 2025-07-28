from pydantic import BaseModel
from typing import Dict, List


def assert_object_contains(actual: Dict, expected_partial: BaseModel):
    """Assert that the actual object contains the expected partial object."""
    expected_dict = expected_partial.model_dump(mode="json")

    for key, value in expected_dict.items():
        assert key in actual, f"Key '{key}' not found in {actual}"
        assert actual[key] == value, f"Expected {key}={value}, got {actual[key]}"


def assert_has_length(actual: List, expected_length: int):
    """Assert that the actual object has the expected length."""
    assert (
        len(actual) == expected_length
    ), f"Expected length {expected_length}, got {len(actual)}"
