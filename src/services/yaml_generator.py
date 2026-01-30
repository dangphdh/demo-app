"""YAML generator for Databricks Metric Views.

Converts Pydantic MetricView models into valid Databricks Metric View YAML.
"""

from typing import Dict, Any
import yaml
from src.models import MetricView, Dimension, Measure, Join, Source


class YAMLGenerator:
    """Generate Databricks Metric View YAML from MetricView models."""

    @staticmethod
    def generate(metric_view: MetricView) -> str:
        """Generate YAML content from a MetricView model.

        Args:
            metric_view: MetricView model instance

        Returns:
            YAML string formatted for Databricks Metric Views
        """
        # Build the YAML structure
        yaml_dict = YAMLGenerator._build_yaml_dict(metric_view)

        # Convert to YAML with proper formatting
        yaml_content = yaml.dump(
            yaml_dict,
            default_flow_style=False,
            sort_keys=False,
            width=80,
            allow_unicode=True
        )

        return yaml_content

    @staticmethod
    def _build_yaml_dict(metric_view: MetricView) -> Dict[str, Any]:
        """Build dictionary representation of the metric view.

        Args:
            metric_view: MetricView model instance

        Returns:
            Dictionary structure for YAML generation
        """
        yaml_dict = {
            "version": 1,
            "name": metric_view.name,
            "catalog": metric_view.catalog,
            "schema": metric_view.schema,
            "description": metric_view.description,
        }

        # Add primary source
        yaml_dict["primary_source"] = metric_view.primary_source

        # Add sources
        yaml_dict["sources"] = YAMLGenerator._build_sources(metric_view.sources)

        # Add dimensions
        if metric_view.dimensions:
            yaml_dict["dimensions"] = YAMLGenerator._build_dimensions(
                metric_view.dimensions
            )

        # Add measures
        yaml_dict["measures"] = YAMLGenerator._build_measures(metric_view.measures)

        # Add joins if present
        if metric_view.joins:
            yaml_dict["joins"] = YAMLGenerator._build_joins(metric_view.joins)

        return yaml_dict

    @staticmethod
    def _build_sources(sources: list[Source]) -> list[Dict[str, Any]]:
        """Build sources section of YAML.

        Args:
            sources: List of Source models

        Returns:
            List of source dictionaries
        """
        sources_list = []

        for source in sources:
            source_dict = {
                "name": source.name,
            }

            if source.type == "table":
                source_dict["table"] = {
                    "catalog": source.catalog,
                    "schema": source.schema,
                    "name": source.table,
                }
            elif source.type == "view":
                source_dict["view"] = {
                    "catalog": source.catalog,
                    "schema": source.schema,
                    "name": source.table,
                }
            elif source.type == "query":
                source_dict["query"] = {
                    "catalog": source.catalog,
                    "schema": source.schema,
                    "query": source.query,
                }

            sources_list.append(source_dict)

        return sources_list

    @staticmethod
    def _build_dimensions(dimensions: list[Dimension]) -> list[Dict[str, Any]]:
        """Build dimensions section of YAML.

        Args:
            dimensions: List of Dimension models

        Returns:
            List of dimension dictionaries
        """
        dimensions_list = []

        for dimension in dimensions:
            dimension_dict = {
                "name": dimension.name,
            }

            if dimension.type == "column":
                dimension_dict["column"] = dimension.column
                if dimension.description:
                    dimension_dict["description"] = dimension.description
                if dimension.data_type:
                    dimension_dict["type"] = dimension.data_type
            elif dimension.type == "custom":
                dimension_dict["expression"] = dimension.expression
                if dimension.description:
                    dimension_dict["description"] = dimension.description
                if dimension.data_type:
                    dimension_dict["type"] = dimension.data_type

            dimensions_list.append(dimension_dict)

        return dimensions_list

    @staticmethod
    def _build_measures(measures: list[Measure]) -> list[Dict[str, Any]]:
        """Build measures section of YAML.

        Args:
            measures: List of Measure models

        Returns:
            List of measure dictionaries
        """
        measures_list = []

        for measure in measures:
            measure_dict = {
                "name": measure.name,
                "expression": measure.expression,
            }

            if measure.description:
                measure_dict["description"] = measure.description

            if measure.data_type:
                measure_dict["type"] = measure.data_type

            measures_list.append(measure_dict)

        return measures_list

    @staticmethod
    def _build_joins(joins: list[Join]) -> list[Dict[str, Any]]:
        """Build joins section of YAML.

        Args:
            joins: List of Join models

        Returns:
            List of join dictionaries
        """
        joins_list = []

        for join in joins:
            join_dict = {
                "left_table": join.left_table,
                "right_table": join.right_table,
                "left_key": join.left_key,
                "right_key": join.right_key,
                "join_type": join.join_type,
            }

            joins_list.append(join_dict)

        return joins_list

    @staticmethod
    def generate_example() -> str:
        """Generate an example metric view YAML for reference.

        Returns:
            Example YAML string
        """
        example_mv = MetricView(
            name="sales_metrics",
            catalog="main",
            schema="analytics",
            description="Core sales metrics for reporting",
            sources=[
                Source(
                    name="orders",
                    type="table",
                    catalog="main",
                    schema="sales",
                    table="orders"
                ),
                Source(
                    name="customers",
                    type="table",
                    catalog="main",
                    schema="sales",
                    table="customers"
                )
            ],
            dimensions=[
                Dimension(
                    name="order_date",
                    type="column",
                    column="order_date",
                    description="Date the order was placed",
                    data_type="date"
                ),
                Dimension(
                    name="customer_region",
                    type="column",
                    column="region",
                    description="Customer geographic region",
                    data_type="string"
                ),
                Dimension(
                    name="order_month",
                    type="custom",
                    expression="DATE_FORMAT(order_date, 'yyyy-MM')",
                    description="Order date formatted as year-month",
                    data_type="string"
                )
            ],
            measures=[
                Measure(
                    name="total_revenue",
                    expression="SUM(order_total)",
                    description="Total revenue from all orders"
                ),
                Measure(
                    name="average_order_value",
                    expression="AVG(order_total)",
                    description="Average order total"
                ),
                Measure(
                    name="order_count",
                    expression="COUNT(*)",
                    description="Total number of orders"
                )
            ],
            joins=[
                Join(
                    left_table="orders",
                    right_table="customers",
                    left_key="customer_id",
                    right_key="id",
                    join_type="inner"
                )
            ],
            primary_source="orders"
        )

        return YAMLGenerator.generate(example_mv)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 80)
    print("Databricks Metric View YAML Example")
    print("=" * 80)
    print()
    print(YAMLGenerator.generate_example())
