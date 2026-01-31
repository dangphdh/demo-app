"""Wizard page - Step-by-step metric view creation."""

import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

# Import components and services
from src.components import SchemaBrowser, DimensionBuilder, MeasureBuilder, JoinVisualizer, YAMLPreview
from src.services import DatabricksClient, TemplateLoader
from src.utils import SessionManager, MetricViewStorage
from src.models import MetricView, Source, Dimension, Measure, Join

# Inject custom theme
from src.ui import inject_theme, page_header, COLORS, SPACING
inject_theme()

st.set_page_config(
    page_title="Wizard - Metric View Builder",
    page_icon="⚡",
    layout="wide"
)


def init_wizard_state():
    """Initialize wizard session state."""
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1

    if "wizard_sources" not in st.session_state:
        st.session_state.wizard_sources = []

    if "wizard_dimensions" not in st.session_state:
        st.session_state.wizard_dimensions = []

    if "wizard_measures" not in st.session_state:
        st.session_state.wizard_measures = []

    if "wizard_joins" not in st.session_state:
        st.session_state.wizard_joins = []

    if "wizard_catalog" not in st.session_state:
        st.session_state.wizard_catalog = "main"

    if "wizard_schema" not in st.session_state:
        st.session_state.wizard_schema = "analytics"

    if "wizard_name" not in st.session_state:
        st.session_state.wizard_name = ""

    if "wizard_description" not in st.session_state:
        st.session_state.wizard_description = ""


def render_header():
    """Render wizard header."""
    page_header(
        "Create Metric View",
        "Follow the steps to configure your metric view"
    )

    # Progress indicator
    steps = [
        "Connect",
        "Sources",
        "Joins",
        "Dimensions",
        "Measures",
        "Review"
    ]

    current_step = st.session_state.wizard_step - 1
    total_steps = len(steps)

    # Progress bar
    st.markdown(f"<p style='margin-bottom: {SPACING['xs']};'><strong>Step {current_step + 1} of {total_steps}:</strong> {steps[current_step]}</p>", unsafe_allow_html=True)
    progress = current_step / (total_steps - 1)
    st.progress(progress)

    # Step indicators
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        if i <= current_step:
            col.markdown(f"**{i+1}. {step}**")
        else:
            col.markdown(f"{i+1}. {step}")


def render_navigation():
    """Render navigation buttons."""
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.session_state.wizard_step > 1:
            if st.button("Previous", use_container_width=True):
                st.session_state.wizard_step -= 1
                st.rerun()

    with col2:
        if st.session_state.wizard_step < 6:
            if st.button("Next", use_container_width=True, type="primary"):
                st.session_state.wizard_step += 1
                st.rerun()

    with col3:
        if st.button("Back to Welcome", use_container_width=True):
            st.switch_page("pages/0_welcome.py")


def step_1_connect():
    """Step 1: Connect to Databricks."""
    st.markdown("### Step 1: Connect to Databricks")

    if not st.session_state.get("user_authenticated"):
        st.warning("Please connect to Databricks from the sidebar first")
        st.info("Use the sidebar to connect using service account or user credentials")
        return False

    st.success("Connected to Databricks!")

    # Show connection info
    config = st.session_state.databricks_config
    st.info(f"Host: `{config.host}`")
    st.info(f"Auth: `{config.auth_method}`")

    return True


def step_2_sources(client: DatabricksClient):
    """Step 2: Select data sources."""
    st.markdown("### Step 2: Select Data Sources")

    # Use schema browser to select tables
    selected_tables = SchemaBrowser.render_multi_select(client, key="wizard_sources")

    if selected_tables:
        st.session_state.wizard_sources = selected_tables
        st.success(f"Selected {len(selected_tables)} table(s)")

        # Show selected tables
        for catalog, schema, table in selected_tables:
            st.text(f"• {catalog}.{schema}.{table}")

        return len(selected_tables) > 0
    else:
        st.info("Select one or more tables from the catalog browser above")
        return False


def step_3_joins():
    """Step 3: Configure joins (if multiple tables)."""
    st.markdown("### Step 3: Configure Joins")

    if len(st.session_state.wizard_sources) < 2:
        st.info("Only one table selected - joins not needed")
        st.session_state.wizard_joins = []
        return True

    st.info("Configure how your tables relate to each other")

    # Convert sources to dict format for join visualizer
    sources = [
        {
            "name": f"{catalog}_{schema}_{table}",
            "catalog": catalog,
            "schema": schema,
            "table": table
        }
        for catalog, schema, table in st.session_state.wizard_sources
    ]

    # Render join visualizer
    joins = JoinVisualizer.render(sources, st.session_state.wizard_joins, key="wizard_joins")
    st.session_state.wizard_joins = joins

    return True


def step_4_dimensions(client: DatabricksClient):
    """Step 4: Define dimensions."""
    st.markdown("### Step 4: Define Dimensions")

    # Get columns from primary source (first table)
    if st.session_state.wizard_sources:
        catalog, schema, table = st.session_state.wizard_sources[0]

        with st.spinner(f"Loading columns for {table}..."):
            success, columns, error = client.get_table_columns(catalog, schema, table)

            if not success:
                st.error(f"Failed to load columns: {error}")
                return False

        # Render dimension builder
        dimensions = DimensionBuilder.render(
            columns,
            st.session_state.wizard_dimensions,
            key="wizard_dimensions"
        )
        st.session_state.wizard_dimensions = dimensions

        if dimensions:
            st.success(f"Defined {len(dimensions)} dimension(s)")

        return len(dimensions) > 0

    return False


def step_5_measures():
    """Step 5: Define measures."""
    st.markdown("### Step 5: Define Measures")

    # Get columns from primary source
    columns = []
    if st.session_state.wizard_sources:
        catalog, schema, table = st.session_state.wizard_sources[0]
        client = DatabricksClient(st.session_state.databricks_config)
        success, columns, error = client.get_table_columns(catalog, schema, table)

    # Render measure builder
    measures = MeasureBuilder.render(
        columns,
        st.session_state.wizard_measures,
        key="wizard_measures"
    )
    st.session_state.wizard_measures = measures

    if measures:
        st.success(f"Defined {len(measures)} measure(s)")

    return len(measures) > 0


def step_6_review():
    """Step 6: Review and generate YAML."""
    st.markdown("### Step 6: Review & Generate")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Metric View Details")

        # Name
        name = st.text_input(
            "Metric View Name *",
            value=st.session_state.wizard_name,
            placeholder="e.g., sales_metrics",
            key="review_name"
        )
        st.session_state.wizard_name = name

        # Catalog and schema
        col1a, col2a = st.columns(2)

        with col1a:
            catalog = st.text_input(
                "Target Catalog *",
                value=st.session_state.wizard_catalog,
                key="review_catalog"
            )
            st.session_state.wizard_catalog = catalog

        with col2a:
            schema_name = st.text_input(
                "Target Schema *",
                value=st.session_state.wizard_schema,
                key="review_schema"
            )
            st.session_state.wizard_schema = schema_name

        # Description
        description = st.text_area(
            "Description",
            value=st.session_state.wizard_description,
            placeholder="What does this metric view contain?",
            key="review_description"
        )
        st.session_state.wizard_description = description

        # Build metric view
        if st.button("Generate Preview", use_container_width=True):
            st.session_state.generate_preview = True

        if st.session_state.get("generate_preview", False):
            metric_view = build_metric_view()

            if metric_view:
                with col2:
                    YAMLPreview.render_summary(metric_view)

                st.markdown("---")

                # YAML Preview
                with st.container():
                    st.markdown(f"<div class='tech-card-header'>Live YAML Preview</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='tech-code-preview'>", unsafe_allow_html=True)
                    YAMLPreview.render(metric_view, show_download=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Deploy button (placeholder for Phase 4)
                if st.button("Deploy to Databricks", type="primary"):
                    st.info("Deployment coming in Phase 4!")

                return True

    return False


def build_metric_view() -> Optional[MetricView]:
    """Build MetricView model from wizard state.

    Returns:
        MetricView object or None if validation fails
    """
    # Validate required fields
    if not st.session_state.wizard_name:
        st.error("Metric View name is required")
        return None

    if not st.session_state.wizard_sources:
        st.error("At least one source is required")
        return None

    if not st.session_state.wizard_measures:
        st.error("At least one measure is required")
        return None

    # Build sources
    sources = []
    for i, (catalog, schema, table) in enumerate(st.session_state.wizard_sources):
        sources.append(Source(
            name=f"source_{i}",
            type="table",
            catalog=catalog,
            schema=schema,
            table=table
        ))

    # Create metric view
    try:
        metric_view = MetricView(
            name=st.session_state.wizard_name,
            catalog=st.session_state.wizard_catalog,
            schema=st.session_state.wizard_schema,
            description=st.session_state.wizard_description,
            sources=sources,
            dimensions=st.session_state.wizard_dimensions,
            measures=st.session_state.wizard_measures,
            joins=st.session_state.wizard_joins,
            primary_source="source_0"
        )

        return metric_view

    except Exception as e:
        st.error(f"Error building metric view: {str(e)}")
        return None


def autosave_wizard_progress():
    """Autosave current wizard progress."""
    try:
        # Build partial metric view from current state
        if st.session_state.wizard_name and st.session_state.wizard_sources:
            sources = []
            for i, (catalog, schema, table) in enumerate(st.session_state.wizard_sources):
                sources.append(Source(
                    name=f"source_{i}",
                    type="table",
                    catalog=catalog,
                    schema=schema,
                    table=table
                ))

            partial_mv = MetricView(
                name=st.session_state.wizard_name,
                catalog=st.session_state.wizard_catalog,
                schema=st.session_state.wizard_schema,
                description=st.session_state.wizard_description,
                sources=sources,
                dimensions=st.session_state.wizard_dimensions,
                measures=st.session_state.wizard_measures,
                joins=st.session_state.wizard_joins,
                primary_source="source_0"
            )

            SessionManager.autosave(partial_mv)
    except Exception:
        # Silent fail for autosave
        pass


def main():
    """Main wizard page."""
    init_wizard_state()

    # Check for autosave recovery
    SessionManager.render_autosave_banner()

    render_header()

    # Get Databricks client if authenticated
    client = None
    if st.session_state.get("user_authenticated"):
        client = DatabricksClient(st.session_state.databricks_config)

    # Render current step
    step_valid = False

    if st.session_state.wizard_step == 1:
        step_valid = step_1_connect()

    elif st.session_state.wizard_step == 2:
        if client:
            step_valid = step_2_sources(client)
        else:
            st.error("Please connect to Databricks first")

    elif st.session_state.wizard_step == 3:
        step_valid = step_3_joins()

    elif st.session_state.wizard_step == 4:
        if client:
            step_valid = step_4_dimensions(client)
        else:
            st.error("Please connect to Databricks first")

    elif st.session_state.wizard_step == 5:
        step_valid = step_5_measures()

    elif st.session_state.wizard_step == 6:
        step_valid = step_6_review()

    # Autosave progress
    autosave_wizard_progress()

    # Navigation
    render_navigation()


if __name__ == "__main__":
    main()
