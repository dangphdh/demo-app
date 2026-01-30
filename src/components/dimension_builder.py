"""Dimension Builder component for creating and editing dimensions."""

import streamlit as st
from typing import List, Dict, Any, Optional
from src.models import Dimension


class DimensionBuilder:
    """Component for building dimensions (column-based and custom)."""

    @staticmethod
    def render(
        available_columns: List[Dict[str, Any]],
        existing_dimensions: List[Dimension],
        key: str = "dimension_builder"
    ) -> List[Dimension]:
        """Render the dimension builder UI.

        Args:
            available_columns: List of available column dictionaries
            existing_dimensions: List of existing Dimension objects
            key: Unique key for this component instance

        Returns:
            Updated list of Dimension objects
        """
        st.subheader("📊 Define Dimensions")

        # Help text
        with st.expander("ℹ️ What is a Dimension?"):
            st.markdown("""
            A **dimension** is a categorical attribute that organizes and filters data,
            such as product names, customer types, or regions.

            **Types of dimensions:**
            - **Column-based**: Directly references a column in your table
            - **Custom**: Uses a SQL expression to create a derived dimension

            **Examples:**
            - `region` - Geographic region of the customer
            - `order_date` - Date when order was placed
            - `order_month` - Extracted as `DATE_FORMAT(order_date, 'yyyy-MM')`
            """)

        # Initialize session state
        if f"{key}_dimensions" not in st.session_state:
            st.session_state[f"{key}_dimensions"] = existing_dimensions.copy()

        dimensions = st.session_state[f"{key}_dimensions"]

        # Show existing dimensions
        if dimensions:
            st.markdown("**Current Dimensions:**")
            for i, dim in enumerate(dimensions):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])

                    with col1:
                        st.text(f"**{dim.name}** ({dim.type})")
                        if dim.type == "column":
                            st.caption(f"Column: `{dim.column}`")
                        else:
                            st.caption(f"Expression: `{dim.expression}`")
                        if dim.description:
                            st.caption(dim.description)

                    with col2:
                        if st.button("✏️", key=f"{key}_edit_{i}"):
                            DimensionBuilder._edit_dimension(i, key)

                    with col3:
                        if st.button("🗑️", key=f"{key}_delete_{i}"):
                            dimensions.pop(i)
                            st.session_state[f"{key}_dimensions"] = dimensions
                            st.rerun()

                    st.markdown("---")

        # Add new dimension section
        st.markdown("#### Add New Dimension")

        # Dimension type selection
        dim_type = st.radio(
            "Dimension Type",
            options=["Column-based", "Custom (SQL Expression)"],
            horizontal=True,
            key=f"{key}_type"
        )

        with st.form(key=f"{key}_add_form"):
            # Name (required)
            name = st.text_input(
                "Dimension Name *",
                placeholder="e.g., customer_region, order_month",
                key=f"{key}_name"
            )

            # Description (optional)
            description = st.text_input(
                "Description",
                placeholder="What does this dimension represent?",
                key=f"{key}_description"
            )

            if dim_type == "Column-based":
                # Column selection
                column_names = [col['name'] for col in available_columns]
                column = st.selectbox(
                    "Select Column *",
                    options=column_names,
                    index=None,
                    placeholder="Choose a column...",
                    key=f"{key}_column"
                )

                # Show column info if selected
                if column:
                    col_info = next((c for c in available_columns if c['name'] == column), None)
                    if col_info:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"📌 Type: `{col_info.get('type', 'UNKNOWN')}`")
                        with col2:
                            if col_info.get('comment'):
                                st.caption(f"💡 {col_info['comment']}")

            else:  # Custom dimension
                expression = st.text_area(
                    "SQL Expression *",
                    placeholder="e.g., DATE_FORMAT(order_date, 'yyyy-MM')",
                    help="Enter a SQL expression to create a custom dimension",
                    key=f"{key}_expression"
                )

                # Show expression examples
                with st.expander("💡 Expression Examples"):
                    st.markdown("""
                    **Date/Time Extraction:**
                    ```
                    DATE_FORMAT(order_date, 'yyyy-MM')
                    YEAR(order_date)
                    MONTH(order_date)
                    ```

                    **String Manipulation:**
                    ```
                    CONCAT(first_name, ' ', last_name)
                    UPPER(customer_segment)
                    SUBSTRING(email, POSITION('@' IN email) + 1)
                    ```

                    **Binning/Bucketing:**
                    ```
                    CASE
                        WHEN revenue < 1000 THEN 'Low'
                        WHEN revenue < 10000 THEN 'Medium'
                        ELSE 'High'
                    END
                    ```
                    """)

            # Submit button
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("➕ Add Dimension", use_container_width=True)
            with col2:
                if st.form_submit_button("Cancel"):
                    st.rerun()

            if submitted:
                if not name:
                    st.error("Dimension name is required")
                elif dim_type == "Column-based" and not column:
                    st.error("Please select a column")
                elif dim_type == "Custom (SQL Expression)" and not expression:
                    st.error("SQL expression is required")
                else:
                    # Create dimension
                    new_dim = Dimension(
                        name=name.strip(),
                        type="column" if dim_type == "Column-based" else "custom",
                        column=column if dim_type == "Column-based" else None,
                        expression=expression if dim_type == "Custom (SQL Expression)" else None,
                        description=description.strip() if description else ""
                    )

                    # Check for duplicates
                    if any(d.name == new_dim.name for d in dimensions):
                        st.error(f"Dimension '{name}' already exists")
                    else:
                        dimensions.append(new_dim)
                        st.session_state[f"{key}_dimensions"] = dimensions
                        st.success(f"✅ Dimension '{name}' added!")
                        st.rerun()

        return dimensions

    @staticmethod
    def _edit_dimension(index: int, key: str):
        """Edit an existing dimension.

        Args:
            index: Index of dimension to edit
            key: Component key
        """
        # Store editing state
        st.session_state[f"{key}_editing"] = index
        st.rerun()

    @staticmethod
    def render_simple(
        available_columns: List[Dict[str, Any]],
        key: str = "simple_dimension_builder"
    ) -> List[Dimension]:
        """Render a simplified dimension builder for quick column selection.

        Args:
            available_columns: List of available column dictionaries
            key: Unique key for this component instance

        Returns:
            List of selected Dimension objects
        """
        st.markdown("**Select Dimensions:**")

        # Initialize session state
        if f"{key}_selected" not in st.session_state:
            st.session_state[f"{key}_selected"] = []

        # Column checkboxes
        selected = []
        for col in available_columns:
            col_name = col['name']
            is_selected = st.checkbox(
                col_name,
                value=col_name in st.session_state[f"{key}_selected"],
                key=f"{key}_{col_name}"
            )
            if is_selected:
                selected.append(col_name)

        st.session_state[f"{key}_selected"] = selected

        # Convert to Dimension objects
        dimensions = [
            Dimension(
                name=col_name,
                type="column",
                column=col_name,
                description=f"Dimension from column {col_name}"
            )
            for col_name in selected
        ]

        return dimensions
