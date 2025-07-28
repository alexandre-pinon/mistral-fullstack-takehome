from pydantic import BaseModel
from typing import Dict, List


def assert_model_contains_model(actual: BaseModel, expected: BaseModel):
    """Assert that the actual model contains the expected model."""
    actual_dict = actual.model_dump(mode="json")
    expected_dict = expected.model_dump(mode="json")
    return assert_object_contains_object(actual_dict, expected_dict)


def assert_object_contains_model(actual: Dict, expected: BaseModel):
    """Assert that the actual object equals the expected object."""
    expected_dict = expected.model_dump(mode="json")
    return assert_object_contains_object(actual, expected_dict)


def assert_object_contains_object(actual: Dict, expected_partial: Dict):
    """Assert that the actual object contains the expected partial object."""
    for key, value in expected_partial.items():
        assert key in actual, f"Key '{key}' not found in {actual}"
        assert actual[key] == value, f"Expected {key}={value}, got {actual[key]}"


def assert_has_length(actual: List, expected_length: int):
    """Assert that the actual object has the expected length."""
    assert (
        len(actual) == expected_length
    ), f"Expected length {expected_length}, got {len(actual)}"
