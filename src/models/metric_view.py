"""Main MetricView model."""

from typing import List, Optional
from pydantic import BaseModel, Field

from .dimension import Dimension
from .measure import Measure
from .join import Join
from .source import Source


class MetricView(BaseModel):
    """Represents a complete Databricks Metric View definition.

    A metric view abstracts complex business logic into a centralized definition,
    enabling consistent metric definitions across reporting tools.
    """

    name: str = Field(..., description="Name of the metric view")
    catalog: str = Field(..., description="Target catalog in Unity Catalog")
    schema: str = Field(..., description="Target schema in Unity Catalog")
    description: str = Field(
        "",
        description="Business-friendly description of this metric view"
    )
    sources: List[Source] = Field(
        ...,
        description="Data sources (tables, views, or queries)"
    )
    dimensions: List[Dimension] = Field(
        default_factory=list,
        description="Dimensions for grouping and filtering"
    )
    measures: List[Measure] = Field(
        ...,
        description="Measures (aggregations) to calculate",
        min_length=1
    )
    joins: List[Join] = Field(
        default_factory=list,
        description="Join relationships between sources"
    )
    primary_source: str = Field(
        ...,
        description="Name of the primary/base source"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "sales_metrics",
                    "catalog": "main",
                    "schema": "analytics",
                    "description": "Core sales metrics for reporting",
                    "sources": [
                        {
                            "name": "orders",
                            "type": "table",
                            "catalog": "main",
                            "schema": "sales",
                            "table": "orders"
                        },
                        {
                            "name": "customers",
                            "type": "table",
                            "catalog": "main",
                            "schema": "sales",
                            "table": "customers"
                        }
                    ],
                    "dimensions": [
                        {
                            "name": "order_date",
                            "type": "column",
                            "column": "order_date",
                            "description": "Date the order was placed"
                        },
                        {
                            "name": "customer_region",
                            "type": "column",
                            "column": "region",
                            "description": "Customer geographic region"
                        }
                    ],
                    "measures": [
                        {
                            "name": "total_revenue",
                            "expression": "SUM(order_total)",
                            "description": "Total revenue from all orders"
                        },
                        {
                            "name": "average_order_value",
                            "expression": "AVG(order_total)",
                            "description": "Average order total"
                        }
                    ],
                    "joins": [
                        {
                            "left_table": "orders",
                            "right_table": "customers",
                            "left_key": "customer_id",
                            "right_key": "id",
                            "join_type": "inner"
                        }
                    ],
                    "primary_source": "orders"
                }
            ]
        }

    def get_source_names(self) -> List[str]:
        """Get list of all source names."""
        return [source.name for source in self.sources]

    def get_dimension_names(self) -> List[str]:
        """Get list of all dimension names."""
        return [dim.name for dim in self.dimensions]

    def get_measure_names(self) -> List[str]:
        """Get list of all measure names."""
        return [measure.name for measure in self.measures]

    def has_joins(self) -> bool:
        """Check if this metric view has joins."""
        return len(self.joins) > 0

    def get_primary_source(self) -> Optional[Source]:
        """Get the primary source object."""
        for source in self.sources:
            if source.name == self.primary_source:
                return source
        return None
