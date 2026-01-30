"""Deploy page - Deploy metric views to Databricks or export YAML."""

import streamlit as st
from typing import Optional
from src.components import YAMLPreview
from src.services import DatabricksClient, YAMLGenerator
from src.utils import MetricViewStorage
from src.models import MetricView

st.set_page_config(
    page_title="Deploy - Metric View Builder",
    page_icon="🚀",
    layout="wide"
)


def init_deploy_state():
    """Initialize deploy session state."""
    if "deploy_metric_view" not in st.session_state:
        st.session_state.deploy_metric_view = None

    if "deploy_yaml" not in st.session_state:
        st.session_state.deploy_yaml = ""

    if "deploy_status" not in st.session_state:
        st.session_state.deploy_status = None


def render_load_section():
    """Render the load metric view section."""
    st.markdown("### 1️⃣ Load Metric View")

    tab1, tab2 = st.tabs(["📝 From Editor", "📤 Upload YAML"])

    with tab1:
        # Check if there's a current metric view from editor
        if st.session_state.get("current_metric_view"):
            mv = st.session_state.current_metric_view

            st.markdown(f"**Current from Editor:** {mv.name}")
            st.caption(f"📍 {mv.catalog}.{mv.schema}")

            if st.button("✅ Use This Metric View", type="primary"):
                st.session_state.deploy_metric_view = mv
                st.session_state.deploy_yaml = YAMLGenerator.generate(mv)
                st.success("✅ Metric view loaded!")
                st.rerun()
        else:
            st.info("No metric view from editor. Go to Editor page first.")
            if st.button("📝 Go to Editor"):
                st.switch_page("pages/2_editor.py")

    with tab2:
        st.markdown("#### Upload YAML File")

        uploaded_file = st.file_uploader(
            "Upload Metric View YAML",
            type=["yaml", "yml"],
            help="Upload a previously generated YAML file"
        )

        if uploaded_file:
            try:
                yaml_content = uploaded_file.getvalue().decode("utf-8")
                mv = MetricViewStorage.import_from_yaml(yaml_content)

                if mv:
                    st.session_state.deploy_metric_view = mv
                    st.session_state.deploy_yaml = yaml_content
                    st.success(f"✅ Loaded: {mv.name}")
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error loading YAML: {str(e)}")


def render_preview_section():
    """Render the preview section."""
    st.markdown("### 2️⃣ Preview & Validate")

    mv = st.session_state.get("deploy_metric_view")

    if not mv:
        st.warning("⚠️ Load a metric view first")
        return

    # Show summary
    YAMLPreview.render_summary(mv)

    st.markdown("---")

    # Show YAML preview
    yaml_content = YAMLPreview.render(mv, show_download=True)
    if yaml_content:
        st.session_state.deploy_yaml = yaml_content


def render_deploy_section():
    """Render the deploy section."""
    st.markdown("### 3️⃣ Deploy to Databricks")

    mv = st.session_state.get("deploy_metric_view")
    yaml_content = st.session_state.get("deploy_yaml", "")

    if not mv or not yaml_content:
        st.warning("⚠️ Load and preview a metric view first")
        return

    # Check authentication
    if not st.session_state.get("user_authenticated"):
        st.error("❌ Please connect to Databricks first (use sidebar)")
        return

    client = DatabricksClient(st.session_state.databricks_config)

    # Deployment options
    st.markdown("#### Deployment Configuration")

    col1, col2 = st.columns(2)

    with col1:
        deploy_name = st.text_input(
            "Metric View Name",
            value=mv.name,
            help="Name for the deployed metric view"
        )

    with col2:
            deploy_catalog = st.text_input(
                "Target Catalog",
                value=mv.catalog,
                help="Target Unity Catalog catalog"
            )

    col3, col4 = st.columns(2)

    with col3:
        deploy_schema = st.text_input(
            "Target Schema",
            value=mv.schema,
            help="Target schema"
        )

    with col4:
        warehouse_id = st.text_input(
            "SQL Warehouse ID",
            value=st.session_state.databricks_config.warehouse_id,
            help="SQL Warehouse for deployment"
        )

    st.markdown("---")

    # Deploy button
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Deploy to Databricks", type="primary", use_container_width=True):
            with st.spinner("Deploying metric view..."):
                success, result_msg, error = client.deploy_metric_view(
                    metric_view_name=deploy_name,
                    catalog=deploy_catalog,
                    schema=deploy_schema,
                    yaml_content=yaml_content,
                    warehouse_id=warehouse_id
                )

                if success:
                    st.session_state.deploy_status = "success"
                    st.success(result_msg)

                    # Show additional info
                    st.info(f"""
                    ✅ **Deployment Successful!**

                    Your metric view has been deployed to Databricks.

                    **Next Steps:**
                    1. Go to Databricks Catalog Explorer
                    2. Navigate to {deploy_catalog}.{deploy_schema}
                    3. Find your metric view: {deploy_name}
                    4. Start querying it with your BI tools!
                    """)
                else:
                    st.session_state.deploy_status = "error"
                    st.error(f"❌ Deployment failed: {error}")

    with col2:
        if st.button("🧪 Test Query", use_container_width=True):
            with st.spinner("Testing metric view query..."):
                success, result, error = client.test_metric_view_query(
                    metric_view_name=deploy_name,
                    catalog=deploy_catalog,
                    schema=deploy_schema,
                    warehouse_id=warehouse_id
                )

                if success:
                    st.success("✅ Test query successful!")
                    st.json(result.manifest.to_dict() if hasattr(result, 'manifest') else {})
                else:
                    st.warning(f"⚠️ Test query returned: {error}")


def render_export_section():
    """Render the export section."""
    st.markdown("### 📥 Export Options")

    mv = st.session_state.get("deploy_metric_view")
    yaml_content = st.session_state.get("deploy_yaml", "")

    if not mv:
        st.warning("⚠️ Load a metric view first")
        return

    # Export options
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Download YAML")

        if yaml_content:
            st.download_button(
                "📥 Download YAML File",
                yaml_content,
                file_name=f"{mv.name}_metric_view.yaml",
                mime="text/yaml",
                use_container_width=True
            )

    with col2:
        st.markdown("#### Copy to Clipboard")

        if st.button("📋 Copy YAML"):
            st.clipboard_copy(yaml_content)
            st.success("✅ Copied to clipboard!")

    with col3:
        st.markdown("#### Save Locally")

        if st.button("💾 Save to App Storage"):
            filepath = MetricViewStorage.save(mv)
            st.success(f"✅ Saved: {filepath}")


def render_manual_instructions():
    """Render manual deployment instructions."""
    st.markdown("### 📖 Manual Deployment Instructions")

    with st.expander("📖 How to Manually Deploy YAML to Databricks", expanded=False):
        st.markdown("""
        #### Step-by-Step Manual Deployment

        1. **Download the YAML**
           - Use the export section above to download your YAML file

        2. **Open Databricks Workspace**
           - Navigate to your Databricks workspace
           - Go to **Catalog** (Data icon in sidebar)

        3. **Navigate to Target Location**
           - Browse to your target catalog and schema
           - Click **Create** → **Metric View**

        4. **Paste YAML Content**
           - Copy the YAML from the file you downloaded
           - Paste it into the metric view editor
           - Or upload the YAML file directly

        5. **Validate and Create**
           - Review the metric view definition
           - Click **Create** to deploy

        6. **Verify Deployment**
           - Navigate to your catalog/schema
           - Find your new metric view
           - Click to view details and dimensions/measures

        #### Querying Your Metric View

        Once deployed, you can query your metric view:

        ```sql
        SELECT
            order_month,
            MEASURE(total_revenue) AS revenue,
            MEASURE(order_count) AS orders
        FROM main.analytics.sales_metrics
        GROUP BY order_month
        ORDER BY order_month
        ```

        #### Using in BI Tools

        - **Power BI**: Connect via Databricks SQL endpoint
        - **Tableau**: Use Databricks connector
        **Looker**: Native Databricks integration
        - **Databricks Dashboards**: Direct integration
        """)


def main():
    """Main deploy page."""
    init_deploy_state()

    st.title("🚀 Deploy Metric View")

    # Check authentication
    if not st.session_state.get("user_authenticated"):
        st.warning("⚠️ Connect to Databricks to enable deployment features")
        st.info("👈 Use the sidebar to connect")

        # Still allow export
        mv = st.session_state.get("deploy_metric_view")
        if mv:
            st.markdown("---")
            render_export_section()
    else:
        # Full deployment flow
        render_load_section()
        st.markdown("---")
        render_preview_section()
        st.markdown("---")
        render_deploy_section()
        st.markdown("---")
        render_export_section()

    # Manual instructions always available
    st.markdown("---")
    render_manual_instructions()

    # Navigation
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏠 Welcome", use_container_width=True):
            st.switch_page("pages/0_welcome.py")

    with col2:
        if st.button("✨ Wizard", use_container_width=True):
            st.switch_page("pages/1_wizard.py")

    with col3:
        if st.button("✏️ Editor", use_container_width=True):
            st.switch_page("pages/2_editor.py")


if __name__ == "__main__":
    main()
