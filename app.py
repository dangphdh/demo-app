"""Databricks Metric View Builder - Main Application

A Streamlit application that allows business users to visually create
Databricks Metric Views without writing YAML or SQL.
"""

import streamlit as st
from src.services import AuthManager, DatabricksClient
from src.utils import show_tutorial_if_active

# Configure Streamlit page
st.set_page_config(
    page_title="Metric View Builder",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "databricks_config" not in st.session_state:
        st.session_state.databricks_config = None

    if "user_authenticated" not in st.session_state:
        st.session_state.user_authenticated = False

    if "current_page" not in st.session_state:
        st.session_state.current_page = "welcome"


def show_sidebar():
    """Display sidebar with navigation and connection status."""
    st.sidebar.title("📊 Metric View Builder")
    st.sidebar.markdown("---")

    # Connection status
    st.sidebar.subheader("Connection Status")

    if st.session_state.user_authenticated and st.session_state.databricks_config:
        config = st.session_state.databricks_config
        st.sidebar.success("✓ Connected")
        st.sidebar.info(f"**Host:** {config.host}")
        st.sidebar.info(f"**Auth:** {config.auth_method}")

        if st.sidebar.button("Disconnect", key="disconnect_btn"):
            st.session_state.user_authenticated = False
            st.session_state.databricks_config = None
            st.rerun()
    else:
        st.sidebar.warning("⚠ Not Connected")

        # Show connection form
        st.sidebar.markdown("#### Connect to Databricks")

        # Check if service account is configured
        has_service = AuthManager.has_service_account_configured()

        if has_service:
            if st.sidebar.button("Use Service Account", key="service_account_btn", use_container_width=True):
                config = AuthManager.get_service_account_config()
                st.session_state.databricks_config = config
                st.session_state.user_authenticated = True
                st.rerun()

        st.sidebar.markdown("**Or use user credentials:**")

        host = st.sidebar.text_input("Host URL", placeholder="https://...")
        token = st.sidebar.text_input("Access Token", type="password")
        warehouse_id = st.sidebar.text_input("Warehouse ID")

        if st.sidebar.button("Connect", key="connect_btn", use_container_width=True):
            if host and token and warehouse_id:
                config = AuthManager.create_user_config(host, token, warehouse_id)
                is_valid, error = AuthManager.validate_config(config)

                if is_valid:
                    # Test connection
                    client = DatabricksClient(config)
                    success, message = client.test_connection()

                    if success:
                        st.session_state.databricks_config = config
                        st.session_state.user_authenticated = True
                        st.sidebar.success(message)
                        st.rerun()
                    else:
                        st.sidebar.error(f"Connection failed: {message}")
                else:
                    st.sidebar.error(f"Invalid config: {error}")
            else:
                st.sidebar.error("Please fill in all fields")

    st.sidebar.markdown("---")


def show_welcome_page():
    """Display welcome page."""
    st.markdown('<h1 class="main-header">Welcome to Metric View Builder</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h3>What is a Metric View?</h3>
        <p>
        A <strong>Metric View</strong> is a centralized way to define and manage consistent,
        reusable, and governed core business metrics in Databricks. Unlike standard views,
        metric views separate measure definitions from dimension groupings, allowing you
        to define metrics once and query them flexibly across any dimension at runtime.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📹 Visual Builder**

        Create metric views without writing YAML or SQL.
        Use our intuitive wizard to define dimensions and measures.
        """)

    with col2:
        st.markdown("""
        **🔗 Smart Joins**

        Connect multiple tables with our visual join interface.
        Support for complex star and snowflake schemas.
        """)

    with col3:
        st.markdown("""
        **🚀 One-Click Deploy**

        Generate YAML or deploy directly to Databricks.
        Support for both service accounts and user credentials.
        """)

    st.markdown("---")
    st.markdown("### Get Started")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✨ Create New", use_container_width=True, type="primary"):
            st.switch_page("src/pages/1_wizard.py")

    with col2:
        if st.button("📝 Load/Edit", use_container_width=True):
            st.switch_page("src/pages/2_editor.py")

    with col3:
        if st.button("🎓 Tutorial", use_container_width=True):
            st.session_state.show_tutorial = True
            st.rerun()

    st.markdown("---")
    st.markdown("### Quick Access to Templates")

    st.markdown("""
    **Pre-built Templates Available:**

    - 💰 **Sales Revenue** - Track sales performance across regions, products, and time
    - 📦 **Order Analytics** - Monitor order pipeline and fulfillment metrics
    - 👥 **Customer Metrics** - Understand customer value and behavior

    👉 Go to **Load/Edit** to start with a template!
    """)


def main():
    """Main application entry point."""
    init_session_state()
    show_sidebar()

    # Show tutorial if activated
    if st.session_state.get("show_tutorial", False):
        from src.utils import render_tutorial
        render_tutorial()
        return

    # Show welcome page
    show_welcome_page()


if __name__ == "__main__":
    main()
