"""Template loader for pre-built metric view templates."""

import json
import os
from typing import List, Dict, Any, Optional
from src.models import MetricView, Source, Dimension, Measure, Join


class Template:
    """Represents a metric view template."""

    def __init__(self, template_data: Dict[str, Any]):
        """Initialize template from JSON data.

        Args:
            template_data: Template configuration dictionary
        """
        self.name = template_data.get("name", "")
        self.title = template_data.get("title", "")
        self.description = template_data.get("description", "")
        self.icon = template_data.get("icon", "📊")
        self.use_case = template_data.get("use_case", "")
        self.data = template_data

    def to_metric_view(self, customizations: Optional[Dict[str, Any]] = None) -> MetricView:
        """Convert template to MetricView model.

        Args:
            customizations: Optional customizations to override template defaults

        Returns:
            MetricView model instance
        """
        data = self.data.copy()

        # Apply customizations
        if customizations:
            data.update(customizations)

        # Build sources
        sources = []
        for source_data in data.get("sources", []):
            sources.append(Source(
                name=source_data["name"],
                type=source_data["type"],
                catalog=source_data["catalog"],
                schema=source_data["schema"],
                table=source_data.get("table"),
                query=source_data.get("query")
            ))

        # Build dimensions
        dimensions = []
        for dim_data in data.get("dimensions", []):
            dimensions.append(Dimension(
                name=dim_data["name"],
                type=dim_data["type"],
                column=dim_data.get("column"),
                expression=dim_data.get("expression"),
                description=dim_data.get("description", ""),
                data_type=dim_data.get("data_type")
            ))

        # Build measures
        measures = []
        for measure_data in data.get("measures", []):
            measures.append(Measure(
                name=measure_data["name"],
                expression=measure_data["expression"],
                description=measure_data.get("description", ""),
                data_type=measure_data.get("data_type")
            ))

        # Build joins
        joins = []
        for join_data in data.get("joins", []):
            joins.append(Join(
                left_table=join_data["left_table"],
                right_table=join_data["right_table"],
                left_key=join_data["left_key"],
                right_key=join_data["right_key"],
                join_type=join_data["join_type"]
            ))

        # Create metric view
        return MetricView(
            name=data.get("name", "metric_view"),
            catalog=data.get("catalog", "main"),
            schema=data.get("schema", "analytics"),
            description=data.get("description", ""),
            sources=sources,
            dimensions=dimensions,
            measures=measures,
            joins=joins,
            primary_source=data.get("primary_source", sources[0].name if sources else "")
        )


class TemplateLoader:
    """Loader for metric view templates."""

    # Template directory
    TEMPLATE_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "templates"
    )

    @staticmethod
    def list_templates() -> List[Template]:
        """List all available templates.

        Returns:
            List of Template objects
        """
        templates = []

        # Template files
        template_files = [
            "sales_revenue.json",
            "order_analytics.json",
            "customer_metrics.json"
        ]

        for filename in template_files:
            filepath = os.path.join(TemplateLoader.TEMPLATE_DIR, filename)

            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        template_data = json.load(f)
                        templates.append(Template(template_data))
                except Exception as e:
                    print(f"Error loading template {filename}: {e}")

        return templates

    @staticmethod
    def get_template(name: str) -> Optional[Template]:
        """Get a specific template by name.

        Args:
            name: Template name (e.g., 'sales_revenue')

        Returns:
            Template object or None if not found
        """
        templates = TemplateLoader.list_templates()

        for template in templates:
            if template.name == name:
                return template

        return None

    @staticmethod
    def render_template_gallery() -> Optional[Template]:
        """Render template gallery UI in Streamlit.

        Returns:
            Selected Template object or None
        """
        st.markdown("### 📋 Template Gallery")

        templates = TemplateLoader.list_templates()

        if not templates:
            st.warning("No templates available")
            return None

        # Display templates in a grid
        cols = st.columns(len(templates))

        selected_template = None

        for i, template in enumerate(templates):
            with cols[i]:
                with st.container():
                    st.markdown(f"### {template.icon}")
                    st.markdown(f"**{template.title}**")
                    st.caption(template.description)
                    st.write(f"*Use case:* {template.use_case}")

                    if st.button(
                        f"Use Template →",
                        key=f"template_{template.name}",
                        use_container_width=True
                    ):
                        selected_template = template

        return selected_template

    @staticmethod
    def render_template_selector() -> Optional[str]:
        """Render simplified template selector.

        Returns:
            Selected template name or None
        """
        templates = TemplateLoader.list_templates()

        if not templates:
            return None

        # Create selection options
        options = {
            t.name: f"{t.icon} {t.title}"
            for t in templates
        }

        # Add blank option
        options[""] = "Start from scratch"

        # Radio button selection
        selected = st.radio(
            "Choose a starting point",
            options=list(options.keys()),
            format_func=lambda x: options.get(x, x),
            index=0,
            horizontal=False
        )

        return selected if selected else None
