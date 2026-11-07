"""Validate JSONPlaceholder comments for the EVTL pipeline.

Author: Abdellah Boudlal
Date: 2026-11

Source: raw JSON response
Sink: validated list of comments
"""

import logging
from typing import Any


def run_validate(
    json_data: Any,
    LOG: logging.Logger,
) -> list[dict[str, Any]]:
    """Validate the response structure and required comment fields."""
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("Top-level type: %s", type(json_data).__name__)

    if not isinstance(json_data, list):
        raise TypeError("Expected JSON data to be a list of comments.")

    if not json_data:
        raise ValueError("Expected at least one comment.")

    if not all(isinstance(record, dict) for record in json_data):
        raise ValueError("Expected each comment to be a dictionary.")

    first_record = json_data[0]
    LOG.info("Keys in first comment: %s", list(first_record))
    for key, value in first_record.items():
        LOG.info("Field %s has type %s", key, type(value).__name__)

    expected_types = {
        "postId": int,
        "id": int,
        "name": str,
        "body": str,
    }

    for index, record in enumerate(json_data, start=1):
        for field, expected_type in expected_types.items():
            if field not in record:
                raise ValueError(f"Comment {index} is missing the field '{field}'.")

            if type(record[field]) is not expected_type:
                raise TypeError(
                    f"Comment {index}: '{field}' must be of type "
                    f"{expected_type.__name__}."
                )

    LOG.info("Validation passed for %d comments.", len(json_data))
    return json_data
