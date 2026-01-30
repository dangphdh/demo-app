"""Validation service for Metric Views.

Provides comprehensive validation for dimensions, measures, joins,
and complete metric views.
"""

from typing import List, Tuple, Optional, Set
from ..models import MetricView, Dimension, Measure, Join, Source


class ValidationError:
    """Represents a validation error with helpful context."""

    def __init__(
        self,
        field: str,
        message: str,
        severity: str = "error",
        suggestion: Optional[str] = None
    ):
        self.field = field
        self.message = message
        self.severity = severity  # "error", "warning"
        self.suggestion = suggestion

    def __str__(self) -> str:
        if self.suggestion:
            return f"{self.severity.upper()}: {self.message}\n  💡 Suggestion: {self.suggestion}"
        return f"{self.severity.upper()}: {self.message}"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "field": self.field,
            "message": self.message,
            "severity": self.severity,
            "suggestion": self.suggestion
        }


class Validator:
    """Validator for Metric Views and their components."""

    @staticmethod
    def validate_metric_view(metric_view: MetricView) -> List[ValidationError]:
        """Validate a complete metric view.

        Args:
            metric_view: MetricView to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors: List[ValidationError] = []

        # Validate basic fields
        if not metric_view.name:
            errors.append(ValidationError(
                "name",
                "Metric view name is required",
                "error",
                "Provide a descriptive name like 'sales_metrics' or 'customer_analytics'"
            ))

        if not metric_view.catalog:
            errors.append(ValidationError(
                "catalog",
                "Catalog name is required",
                "error",
                "Specify the Unity Catalog catalog (e.g., 'main')"
            ))

        if not metric_view.schema:
            errors.append(ValidationError(
                "schema",
                "Schema name is required",
                "error",
                "Specify the schema name (e.g., 'analytics')"
            ))

        # Validate sources
        if not metric_view.sources:
            errors.append(ValidationError(
                "sources",
                "At least one source is required",
                "error"
            ))
        else:
            errors.extend(Validator._validate_sources(metric_view))

        # Validate primary source
        if not metric_view.primary_source:
            errors.append(ValidationError(
                "primary_source",
                "Primary source must be specified",
                "error",
                "Select the main/base table for your metric view"
            ))
        else:
            source_names = [s.name for s in metric_view.sources]
            if metric_view.primary_source not in source_names:
                errors.append(ValidationError(
                    "primary_source",
                    f"Primary source '{metric_view.primary_source}' not found in sources",
                    "error",
                    f"Choose from: {', '.join(source_names)}"
                ))

        # Validate dimensions
        if metric_view.dimensions:
            errors.extend(Validator._validate_dimensions(metric_view))

        # Validate measures
        if not metric_view.measures:
            errors.append(ValidationError(
                "measures",
                "At least one measure is required",
                "error",
                "Add measures like SUM, COUNT, or AVG to aggregate your data"
            ))
        else:
            errors.extend(Validator._validate_measures(metric_view))

        # Validate joins
        if metric_view.joins:
            errors.extend(Validator._validate_joins(metric_view))

        # Check for duplicate names
        errors.extend(Validator._check_duplicate_names(metric_view))

        return errors

    @staticmethod
    def _validate_sources(metric_view: MetricView) -> List[ValidationError]:
        """Validate sources in the metric view."""
        errors: List[ValidationError] = []
        source_names: Set[str] = set()

        for i, source in enumerate(metric_view.sources):
            if not source.name:
                errors.append(ValidationError(
                    f"sources[{i}]",
                    "Source name is required",
                    "error"
                ))
                continue

            if source.name in source_names:
                errors.append(ValidationError(
                    f"sources[{i}]",
                    f"Duplicate source name: '{source.name}'",
                    "error",
                    "Use unique names for each source"
                ))
            source_names.add(source.name)

            # Validate based on source type
            if source.type == "table":
                if not source.table:
                    errors.append(ValidationError(
                        f"sources[{i}].table",
                        f"Table name is required for source '{source.name}'",
                        "error"
                    ))
            elif source.type == "query":
                if not source.query:
                    errors.append(ValidationError(
                        f"sources[{i}].query",
                        f"SQL query is required for source '{source.name}'",
                        "error"
                    ))
                # Basic SQL syntax check
                if source.query and not source.query.strip().upper().startswith("SELECT"):
                    errors.append(ValidationError(
                        f"sources[{i}].query",
                        f"Query should start with SELECT",
                        "warning"
                    ))

        return errors

    @staticmethod
    def _validate_dimensions(metric_view: MetricView) -> List[ValidationError]:
        """Validate dimensions in the metric view."""
        errors: List[ValidationError] = []
        dim_names: Set[str] = set()

        # Get available columns from sources
        available_columns = set()
        for source in metric_view.sources:
            if source.type == "table" and source.table:
                # We can't actually validate column references without schema
                # This would be enhanced with Databricks schema info
                pass

        for i, dimension in enumerate(metric_view.dimensions):
            if not dimension.name:
                errors.append(ValidationError(
                    f"dimensions[{i}]",
                    "Dimension name is required",
                    "error"
                ))
                continue

            if dimension.name in dim_names:
                errors.append(ValidationError(
                    f"dimensions[{i}]",
                    f"Duplicate dimension name: '{dimension.name}'",
                    "error"
                ))
            dim_names.add(dimension.name)

            # Validate based on dimension type
            if dimension.type == "column":
                if not dimension.column:
                    errors.append(ValidationError(
                        f"dimensions[{i}].column",
                        f"Column name is required for dimension '{dimension.name}'",
                        "error"
                    ))
            elif dimension.type == "custom":
                if not dimension.expression:
                    errors.append(ValidationError(
                        f"dimensions[{i}].expression",
                        f"SQL expression is required for custom dimension '{dimension.name}'",
                        "error"
                    ))
                else:
                    # Basic SQL syntax validation
                    errors.extend(Validator._validate_sql_expression(
                        dimension.expression,
                        f"dimensions[{i}].expression",
                        dimension.name
                    ))

        return errors

    @staticmethod
    def _validate_measures(metric_view: MetricView) -> List[ValidationError]:
        """Validate measures in the metric view."""
        errors: List[ValidationError] = []
        measure_names: Set[str] = set()

        for i, measure in enumerate(metric_view.measures):
            if not measure.name:
                errors.append(ValidationError(
                    f"measures[{i}]",
                    "Measure name is required",
                    "error"
                ))
                continue

            if measure.name in measure_names:
                errors.append(ValidationError(
                    f"measures[{i}]",
                    f"Duplicate measure name: '{measure.name}'",
                    "error"
                ))
            measure_names.add(measure.name)

            if not measure.expression:
                errors.append(ValidationError(
                    f"measures[{i}].expression",
                    f"Expression is required for measure '{measure.name}'",
                    "error"
                ))
            else:
                # Validate measure expression
                errors.extend(Validator._validate_measure_expression(
                    measure.expression,
                    f"measures[{i}].expression",
                    measure.name
                ))

        return errors

    @staticmethod
    def _validate_joins(metric_view: MetricView) -> List[ValidationError]:
        """Validate joins in the metric view."""
        errors: List[ValidationError] = []
        source_names = {s.name for s in metric_view.sources}

        for i, join in enumerate(metric_view.joins):
            # Validate table references
            if join.left_table not in source_names:
                errors.append(ValidationError(
                    f"joins[{i}].left_table",
                    f"Left table '{join.left_table}' not found in sources",
                    "error",
                    f"Available sources: {', '.join(sorted(source_names))}"
                ))

            if join.right_table not in source_names:
                errors.append(ValidationError(
                    f"joins[{i}].right_table",
                    f"Right table '{join.right_table}' not found in sources",
                    "error",
                    f"Available sources: {', '.join(sorted(source_names))}"
                ))

            if not join.left_key:
                errors.append(ValidationError(
                    f"joins[{i}].left_key",
                    "Left key column is required",
                    "error"
                ))

            if not join.right_key:
                errors.append(ValidationError(
                    f"joins[{i}].right_key",
                    "Right key column is required",
                    "error"
                ))

        # Check for circular joins
        errors.extend(Validator._detect_circular_joins(metric_view.joins))

        return errors

    @staticmethod
    def _validate_sql_expression(
        expression: str,
        field: str,
        context: str
    ) -> List[ValidationError]:
        """Basic SQL expression validation."""
        errors: List[ValidationError] = []

        # Check for obvious SQL injection patterns
        dangerous_patterns = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE"]
        expr_upper = expression.upper()

        for pattern in dangerous_patterns:
            if pattern in expr_upper:
                errors.append(ValidationError(
                    field,
                    f"Potentially dangerous SQL pattern detected: '{pattern}'",
                    "error",
                    "This pattern may indicate SQL injection or data modification"
                ))

        return errors

    @staticmethod
    def _validate_measure_expression(
        expression: str,
        field: str,
        measure_name: str
    ) -> List[ValidationError]:
        """Validate measure-specific expressions."""
        errors: List[ValidationError] = []

        # Check for aggregate functions (measures should aggregate)
        aggregates = ["SUM(", "COUNT(", "AVG(", "MIN(", "MAX(",
                     "STDDEV(", "VARIANCE("]
        expr_upper = expression.upper()

        has_aggregate = any(agg in expr_upper for agg in aggregates)

        if not has_aggregate and not expression.startswith("COUNT("):
            errors.append(ValidationError(
                field,
                f"Measure '{measure_name}' doesn't appear to use an aggregate function",
                "warning",
                "Measures typically use aggregate functions like SUM, COUNT, or AVG"
            ))

        # Check for division by zero risk
        if "/" in expression:
            errors.append(ValidationError(
                field,
                f"Measure '{measure_name}' contains division - ensure denominator is never zero",
                "warning",
                "Consider using CASE WHEN denominator = 0 THEN 0 ELSE numerator/denominator END"
            ))

        # Basic SQL validation
        errors.extend(Validator._validate_sql_expression(expression, field, measure_name))

        return errors

    @staticmethod
    def _detect_circular_joins(joins: List[Join]) -> List[ValidationError]:
        """Detect circular join dependencies."""
        errors: List[ValidationError] = []

        if not joins:
            return errors

        # Build adjacency list for join graph
        graph = {}
        for join in joins:
            if join.left_table not in graph:
                graph[join.left_table] = []
            graph[join.left_table].append(join.right_table)

        # Simple cycle detection using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(node: str, path: List[str] = None) -> bool:
            if path is None:
                path = []

            visited.add(node)
            rec_stack.add(node)
            path = path + [node]

            if node in graph:
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        if has_cycle(neighbor, path):
                            return True
                    elif neighbor in rec_stack:
                        # Found a cycle
                        cycle_path = path[path.index(neighbor):] + [neighbor]
                        errors.append(ValidationError(
                            "joins",
                            f"Circular join detected: {' -> '.join(cycle_path)}",
                            "error",
                            "Remove one of the joins to break the cycle"
                        ))
                        return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                has_cycle(node)

        return errors

    @staticmethod
    def _check_duplicate_names(metric_view: MetricView) -> List[ValidationError]:
        """Check for duplicate names across dimensions and measures."""
        errors: List[ValidationError] = []

        dim_names = {d.name for d in metric_view.dimensions}
        measure_names = {m.name for m in metric_view.measures}

        # Check for overlap
        overlap = dim_names & measure_names
        if overlap:
            for name in overlap:
                errors.append(ValidationError(
                    "naming",
                    f"Name conflict: '{name}' is used as both a dimension and a measure",
                    "error",
                    f"Rename either the dimension or the measure to use unique names"
                ))

        return errors
