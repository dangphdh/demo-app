"""Measure model for metric views."""

from typing import Optional
from pydantic import BaseModel, Field


class Measure(BaseModel):
    """Represents a measure in a metric view.

    A measure is a value that summarizes business activity, typically using
    an aggregate function such as SUM() or AVG().
    """

    name: str = Field(..., description="Unique name for the measure")
    expression: str = Field(
        ...,
        description="SQL expression defining the measure (e.g., 'SUM(revenue)', 'COUNT(DISTINCT customer_id)')"
    )
    description: str = Field(
        "",
        description="Business-friendly description of what this measure calculates"
    )
    data_type: Optional[str] = Field(
        None,
        description="Return data type of the measure expression"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "total_revenue",
                    "expression": "SUM(order_total)",
                    "description": "Sum of all order totals",
                    "data_type": "decimal"
                },
                {
                    "name": "revenue_per_customer",
                    "expression": "SUM(revenue) / COUNT(DISTINCT customer_id)",
                    "description": "Average revenue per unique customer",
                    "data_type": "decimal"
                },
                {
                    "name": "order_count",
                    "expression": "COUNT(*)",
                    "description": "Total number of orders",
                    "data_type": "bigint"
                }
            ]
        }
