"""Source model for metric views."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Represents a data source for a metric view.

    A source can be a table, view, or SQL query.
    """

    name: str = Field(..., description="Unique name/alias for this source")
    type: Literal["table", "view", "query"] = Field(
        "table",
        description="Type of data source"
    )
    catalog: str = Field(..., description="Databricks catalog name")
    schema: str = Field(..., description="Database schema name")
    table: Optional[str] = Field(
        None,
        description="Table or view name (for table/view sources)"
    )
    query: Optional[str] = Field(
        None,
        description="SQL query (for query sources)"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "orders",
                    "type": "table",
                    "catalog": "main",
                    "schema": "sales",
                    "table": "orders"
                },
                {
                    "name": "customer_summary",
                    "type": "query",
                    "catalog": "main",
                    "schema": "sales",
                    "query": "SELECT customer_id, SUM(total) as total_spent FROM orders GROUP BY customer_id"
                }
            ]
        }

    def get_full_name(self) -> str:
        """Get the full qualified name for table/view sources."""
        if self.type in ["table", "view"] and self.table:
            return f"{self.catalog}.{self.schema}.{self.table}"
        return self.name
