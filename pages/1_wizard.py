"""Wizard page - Step-by-step metric view creation."""

import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

# Import components and services
from src.components import SchemaBrowser, DimensionBuilder, MeasureBuilder, YAMLPreview
from src.services import DatabricksClient, TemplateLoader
from src.utils import SessionManager, MetricViewStorage
from src.models import MetricView, Source, Dimension, Measure

st.set_page_config(
    page_title="Wizard - Metric View Builder",
    page_icon="✨",
    layout="wide"
)


def init_wizard_state():
    """Initialize wizard session state."""
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1

    if "wizard_source" not in st.session_state:
        st.session_state.wizard_source = None  # Single source instead of list

    if "wizard_dimensions" not in st.session_state:
        st.session_state.wizard_dimensions = []

    if "wizard_measures" not in st.session_state:
        st.session_state.wizard_measures = []

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
    st.title("✨ Create Metric View - Wizard")
    st.markdown("Follow the steps to create your Databricks Metric View.")

    # Progress indicator
    steps = [
        "1️⃣ Connect",
        "2️⃣ Source",
        "3️⃣ Dimensions",
        "4️⃣ Measures",
        "5️⃣ Review"
    ]

    current_step = st.session_state.wizard_step - 1

    # Progress bar
    progress = current_step / (len(steps) - 1)
    st.progress(progress)

    # Step indicators
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        if i <= current_step:
            col.markdown(f"**{step}**")
        else:
            col.markdown(f"{step}")


def render_navigation():
    """Render navigation buttons."""
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.session_state.wizard_step > 1:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.wizard_step -= 1
                st.rerun()

    with col2:
        if st.session_state.wizard_step < 5:
            if st.button("Next ➡️", use_container_width=True, type="primary"):
                st.session_state.wizard_step += 1
                st.rerun()

    with col3:
        if st.button("🏠 Back to Welcome", use_container_width=True):
            st.switch_page("pages/0_welcome.py")


def step_1_connect():
    """Step 1: Connect to Databricks."""
    st.markdown("### Step 1: Connect to Databricks")

    if not st.session_state.get("user_authenticated"):
        st.warning("⚠️ Please connect to Databricks from the sidebar first")
        st.info("👈 Use the sidebar to connect using service account or user credentials")
        return False

    st.success("✅ Connected to Databricks!")

    # Show connection info
    config = st.session_state.databricks_config
    st.info(f"🔗 Host: `{config.host}`")
    st.info(f"🔑 Auth: `{config.auth_method}`")

    return True


def step_2_sources(client: DatabricksClient):
    """Step 2: Select data source."""
    st.markdown("### Step 2: Select Data Source")

    st.info("ℹ️ Select a single table for your metric view")

    # Use schema browser to select tables (limit to one)
    selected_tables = SchemaBrowser.render_multi_select(client, key="wizard_source")

    if selected_tables and len(selected_tables) > 0:
        # Take only the first selected table
        selected_table = selected_tables[0]
        st.session_state.wizard_source = selected_table
        catalog, schema, table = selected_table
        st.success(f"✅ Selected table: {catalog}.{schema}.{table}")
        if len(selected_tables) > 1:
            st.warning("⚠️ Only the first selected table will be used (single-table mode)")
        return True
    else:
        st.info("👆 Select a table from the catalog browser above")
        return False


def step_3_dimensions(client: DatabricksClient):
    """Step 3: Define dimensions."""
    st.markdown("### Step 3: Define Dimensions")

    # Get columns from selected table
    if st.session_state.wizard_source:
        catalog, schema, table = st.session_state.wizard_source

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
            st.success(f"✅ Defined {len(dimensions)} dimension(s)")
        return True

    return False


def step_4_measures():
    """Step 4: Define measures."""
    st.markdown("### Step 4: Define Measures")

    # Get columns from selected source
    columns = []
    if st.session_state.wizard_source:
        catalog, schema, table = st.session_state.wizard_source
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
        st.success(f"✅ Defined {len(measures)} measure(s)")

    return len(measures) > 0


def step_5_review():
    """Step 5: Review and generate YAML."""
    st.markdown("### Step 5: Review & Generate")

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
        if st.button("🔄 Generate Preview", use_container_width=True):
            st.session_state.generate_preview = True

        if st.session_state.get("generate_preview", False):
            metric_view = build_metric_view()

            if metric_view:
                with col2:
                    YAMLPreview.render_summary(metric_view)

                st.markdown("---")
                YAMLPreview.render(metric_view, show_download=True)

                # Deploy button (placeholder for Phase 4)
                if st.button("🚀 Deploy to Databricks", type="primary"):
                    st.info("🚀 Deployment coming in Phase 4!")

                return True

    return False



def build_metric_view() -> Optional[MetricView]:
    """Build MetricView model from wizard state.

    Returns:
        MetricView object or None if validation fails
    """
    # Validate required fields
    if not st.session_state.wizard_name:
        st.error("❌ Metric View name is required")
        return None

    if not st.session_state.wizard_source:
        st.error("❌ A source table is required")
        return None

    if not st.session_state.wizard_measures:
        st.error("❌ At least one measure is required")
        return None

    # Build source from single table
    catalog, schema, table = st.session_state.wizard_source
    source = Source(
        name="primary_source",
        type="table",
        catalog=catalog,
        schema=schema,
        table=table
    )

    # Create metric view
    try:
        metric_view = MetricView(
            name=st.session_state.wizard_name,
            catalog=st.session_state.wizard_catalog,
            schema=st.session_state.wizard_schema,
            description=st.session_state.wizard_description,
            sources=[source],
            dimensions=st.session_state.wizard_dimensions,
            measures=st.session_state.wizard_measures,
            joins=[],  # Empty joins for single-table metric views
            primary_source="primary_source"
        )

        return metric_view

    except Exception as e:
        st.error(f"❌ Error building metric view: {str(e)}")
        return None


def autosave_wizard_progress():
    """Autosave current wizard progress."""
    try:
        # Build partial metric view from current state
        if st.session_state.wizard_name and st.session_state.wizard_source:
            catalog, schema, table = st.session_state.wizard_source
            source = Source(
                name="primary_source",
                type="table",
                catalog=catalog,
                schema=schema,
                table=table
            )

            partial_mv = MetricView(
                name=st.session_state.wizard_name,
                catalog=st.session_state.wizard_catalog,
                schema=st.session_state.wizard_schema,
                description=st.session_state.wizard_description,
                sources=[source],
                dimensions=st.session_state.wizard_dimensions,
                measures=st.session_state.wizard_measures,
                joins=[],  # Empty joins for single-table metric views
                primary_source="primary_source"
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
            st.error("❌ Please connect to Databricks first")

    elif st.session_state.wizard_step == 3:
        if client:
            step_valid = step_3_dimensions(client)
        else:
            st.error("❌ Please connect to Databricks first")

    elif st.session_state.wizard_step == 4:
        step_valid = step_4_measures()

    elif st.session_state.wizard_step == 5:
        step_valid = step_5_review()

    # Autosave progress
    autosave_wizard_progress()

    # Navigation
    render_navigation()


if __name__ == "__main__":
    main()
