"""Join model for metric views."""

from typing import Literal
from pydantic import BaseModel, Field


class Join(BaseModel):
    """Represents a join relationship between two tables in a metric view.

    Defines how to connect tables when building metric views from multiple sources.
    """

    left_table: str = Field(..., description="Name of the left table")
    right_table: str = Field(..., description="Name of the right table")
    left_key: str = Field(..., description="Column name to join on in the left table")
    right_key: str = Field(..., description="Column name to join on in the right table")
    join_type: Literal["inner", "left", "right", "full"] = Field(
        "inner",
        description="Type of join: inner, left, right, or full outer"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "left_table": "orders",
                    "right_table": "customers",
                    "left_key": "customer_id",
                    "right_key": "id",
                    "join_type": "inner"
                },
                {
                    "left_table": "orders",
                    "right_table": "products",
                    "left_key": "product_id",
                    "right_key": "id",
                    "join_type": "left"
                }
            ]
        }
