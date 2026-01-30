"""Dimension model for metric views."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class Dimension(BaseModel):
    """Represents a dimension in a metric view.

    A dimension is a categorical attribute that organizes and filters data,
    such as product names, customer types, or regions.
    """

    name: str = Field(..., description="Unique name for the dimension")
    type: Literal["column", "custom"] = Field(
        ...,
        description="Type of dimension: direct column reference or custom SQL expression"
    )
    column: Optional[str] = Field(
        None,
        description="Column name (for column-type dimensions)"
    )
    expression: Optional[str] = Field(
        None,
        description="SQL expression (for custom dimensions)"
    )
    description: str = Field(
        "",
        description="Business-friendly description of what this dimension represents"
    )
    data_type: Optional[str] = Field(
        None,
        description="Data type (string, int, timestamp, etc.)"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "region",
                    "type": "column",
                    "column": "customer_region",
                    "description": "Geographic region of the customer",
                    "data_type": "string"
                },
                {
                    "name": "order_month",
                    "type": "custom",
                    "expression": "DATE_FORMAT(order_date, 'yyyy-MM')",
                    "description": "Order date formatted as year-month",
                    "data_type": "string"
                }
            ]
        }
