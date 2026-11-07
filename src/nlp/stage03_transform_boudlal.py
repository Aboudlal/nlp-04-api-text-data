"""Transform validated JSONPlaceholder comments into a Polars DataFrame.

Author: Abdellah Boudlal
Date: 2026-11
"""

import logging
from typing import Any

import polars as pl


def run_transform(
    json_data: list[dict[str, Any]],
    LOG: logging.Logger,
) -> pl.DataFrame:
    """Select comment fields and count words in each comment body."""
    LOG.info("STAGE 03: TRANSFORM starting...")

    records = [
        {
            "post_id": record["postId"],
            "comment_id": record["id"],
            "name": record["name"],
            "body": record["body"],
        }
        for record in json_data
    ]

    df = pl.DataFrame(records).with_columns(
        pl.col("body").str.count_matches(r"\S+").alias("body_word_count")
    )

    LOG.info("Transformed %d comments.", df.height)
    return df
