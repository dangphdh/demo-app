"""Schema Browser component for browsing Databricks Unity Catalog.

Provides a tree-view interface to browse catalogs, schemas, and tables.
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Tuple
from src.services import DatabricksClient


class SchemaBrowser:
    """Component for browsing Databricks schemas."""

    @staticmethod
    def render(
        client: DatabricksClient,
        key: str = "schema_browser"
    ) -> Optional[Tuple[str, str, str]]:
        """Render the schema browser UI.

        Args:
            client: DatabricksClient instance
            key: Unique key for this component instance

        Returns:
            Tuple of (catalog, schema, table) if selected, None otherwise
        """
        st.subheader("📁 Browse Databricks Catalog")

        # Initialize session state
        if f"{key}_catalogs" not in st.session_state:
            st.session_state[f"{key}_catalogs"] = []
            st.session_state[f"{key}_schemas"] = {}
            st.session_state[f"{key}_tables"] = {}
            st.session_state[f"{key}_selected_catalog"] = None
            st.session_state[f"{key}_selected_schema"] = None
            st.session_state[f"{key}_selected_table"] = None

        # Load catalogs if not loaded
        if not st.session_state[f"{key}_catalogs"]:
            with st.spinner("Loading catalogs..."):
                success, catalogs, error = client.list_catalogs()
                if success:
                    st.session_state[f"{key}_catalogs"] = catalogs
                else:
                    st.error(f"Failed to load catalogs: {error}")
                    return None

        # Catalog selection
        catalog = st.selectbox(
            "Select Catalog",
            options=st.session_state[f"{key}_catalogs"],
            index=None,
            key=f"{key}_catalog_select",
            placeholder="Choose a catalog..."
        )

        if not catalog:
            st.info("👆 Select a catalog to begin")
            return None

        # Load schemas for selected catalog
        if catalog != st.session_state[f"{key}_selected_catalog"]:
            st.session_state[f"{key}_selected_catalog"] = catalog
            st.session_state[f"{key}_selected_schema"] = None
            with st.spinner(f"Loading schemas for {catalog}..."):
                success, schemas, error = client.list_schemas(catalog)
                if success:
                    st.session_state[f"{key}_schemas"][catalog] = schemas
                else:
                    st.error(f"Failed to load schemas: {error}")
                    return None

        # Schema selection
        schemas = st.session_state[f"{key}_schemas"].get(catalog, [])
        schema = st.selectbox(
            "Select Schema",
            options=schemas,
            index=None,
            key=f"{key}_schema_select",
            placeholder="Choose a schema..."
        )

        if not schema:
            st.info("👆 Select a schema to view tables")
            return None

        # Load tables for selected schema
        full_name = f"{catalog}.{schema}"
        if schema != st.session_state[f"{key}_selected_schema"]:
            st.session_state[f"{key}_selected_schema"] = schema
            st.session_state[f"{key}_selected_table"] = None
            with st.spinner(f"Loading tables for {full_name}..."):
                success, tables, error = client.list_tables(catalog, schema)
                if success:
                    st.session_state[f"{key}_tables"][full_name] = tables
                else:
                    st.error(f"Failed to load tables: {error}")
                    return None

        # Table selection
        tables = st.session_state[f"{key}_tables"].get(full_name, [])
        table_options = [f"{t['name']} ({t['type']})" for t in tables]
        table_display = st.selectbox(
            "Select Table",
            options=table_options,
            index=None,
            key=f"{key}_table_select",
            placeholder="Choose a table..."
        )

        if table_display:
            # Extract table name from display string
            table = table_display.split(" (")[0]

            # Show table details
            selected_table_info = next(
                (t for t in tables if t['name'] == table),
                None
            )

            if selected_table_info and selected_table_info.get('comment'):
                st.caption(f"💡 {selected_table_info['comment']}")

            st.session_state[f"{key}_selected_table"] = table

            return catalog, schema, table

        return None

    @staticmethod
    def render_multi_select(
        client: DatabricksClient,
        key: str = "schema_browser_multi"
    ) -> List[Tuple[str, str, str]]:
        """Render schema browser with multi-table selection.

        Args:
            client: DatabricksClient instance
            key: Unique key for this component instance

        Returns:
            List of (catalog, schema, table) tuples
        """
        st.subheader("📁 Select Tables")

        # Initialize session state
        if f"{key}_selected_tables" not in st.session_state:
            st.session_state[f"{key}_selected_tables"] = []

        # Use single select to add tables
        selection = SchemaBrowser.render(client, key=key)

        col1, col2 = st.columns(2)

        with col1:
            if selection and st.button("➕ Add Table", key=f"{key}_add"):
                catalog, schema, table = selection
                current = st.session_state[f"{key}_selected_tables"]
                if (catalog, schema, table) not in current:
                    st.session_state[f"{key}_selected_tables"].append(
                        (catalog, schema, table)
                    )
                    st.rerun()

        with col2:
            if st.session_state[f"{key}_selected_tables"] and st.button(
                "🗑️ Clear All",
                key=f"{key}_clear"
            ):
                st.session_state[f"{key}_selected_tables"] = []
                st.rerun()

        # Show selected tables
        if st.session_state[f"{key}_selected_tables"]:
            st.markdown("**Selected Tables:**")
            for i, (catalog, schema, table) in enumerate(
                st.session_state[f"{key}_selected_tables"]
            ):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(f"• {catalog}.{schema}.{table}")
                with col2:
                    if st.button("❌", key=f"{key}_remove_{i}"):
                        st.session_state[f"{key}_selected_tables"].pop(i)
                        st.rerun()

        return st.session_state[f"{key}_selected_tables"]

    @staticmethod
    def get_table_columns(
        client: DatabricksClient,
        catalog: str,
        schema: str,
        table: str
    ) -> Tuple[bool, List[Dict[str, Any]], Optional[str]]:
        """Get column information for a table.

        Args:
            client: DatabricksClient instance
            catalog: Catalog name
            schema: Schema name
            table: Table name

        Returns:
            Tuple of (success, columns_list, error_message)
        """
        return client.get_table_columns(catalog, schema, table)

    @staticmethod
    def render_columns(
        client: DatabricksClient,
        catalog: str,
        schema: str,
        table: str,
        key: str = "columns_browser"
    ) -> List[Dict[str, Any]]:
        """Render column information for a table.

        Args:
            client: DatabricksClient instance
            catalog: Catalog name
            schema: Schema name
            table: Table name
            key: Unique key for this component instance

        Returns:
            List of column dictionaries
        """
        st.subheader(f"📋 Columns in {catalog}.{schema}.{table}")

        success, columns, error = SchemaBrowser.get_table_columns(
            client, catalog, schema, table
        )

        if not success:
            st.error(f"Failed to load columns: {error}")
            return []

        # Display columns in a nice format
        st.markdown(f"**{len(columns)} columns found**")

        # Create DataFrame for display
        import pandas as pd

        df = pd.DataFrame(columns)
        df_display = df[['name', 'type', 'nullable']]

        if 'comment' in df.columns:
            df_display['comment'] = df['comment']

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

        return columns
