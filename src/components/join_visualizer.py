"""Join Visualizer component for configuring table joins."""

import streamlit as st
from typing import List, Dict, Any, Optional
from ..models import Join


class JoinVisualizer:
    """Component for visualizing and configuring table joins."""

    @staticmethod
    def render(
        sources: List[Dict[str, str]],
        existing_joins: List[Join],
        key: str = "join_visualizer"
    ) -> List[Join]:
        """Render the join visualizer UI.

        Args:
            sources: List of source dictionaries with 'name' key
            existing_joins: List of existing Join objects
            key: Unique key for this component instance

        Returns:
            Updated list of Join objects
        """
        st.subheader("🔗 Configure Joins")

        # Help text
        with st.expander("ℹ️ Understanding Joins"):
            st.markdown("""
            **Joins** allow you to combine data from multiple tables.

            **Join Types:**
            - **Inner Join**: Only matching rows from both tables
            - **Left Join**: All rows from left table, plus matching from right
            - **Right Join**: All rows from right table, plus matching from left
            - **Full Join**: All rows from both tables

            **Example:**
            If you have `orders` and `customers` tables:
            - Left table: `orders`
            - Right table: `customers`
            - Left key: `customer_id` (in orders)
            - Right key: `id` (in customers)
            """)

        # Check if multiple sources available
        if len(sources) < 2:
            st.info("💡 Add at least 2 tables to configure joins")
            return existing_joins

        # Initialize session state
        if f"{key}_joins" not in st.session_state:
            st.session_state[f"{key}_joins"] = existing_joins.copy()

        joins = st.session_state[f"{key}_joins"]

        # Show existing joins
        if joins:
            st.markdown("**Current Joins:**")
            for i, join in enumerate(joins):
                with st.container():
                    col1, col2, col3 = st.columns([5, 1, 1])

                    with col1:
                        st.markdown(
                            f"**{join.left_table}**.{join.left_key} "
                            f"←[{join.join_type.upper()}]→ "
                            f"**{join.right_table}**.{join.right_key}"
                        )

                    with col2:
                        if st.button("✏️", key=f"{key}_edit_{i}"):
                            JoinVisualizer._edit_join(i, key)

                    with col3:
                        if st.button("🗑️", key=f"{key}_delete_{i}"):
                            joins.pop(i)
                            st.session_state[f"{key}_joins"] = joins
                            st.rerun()

                    st.markdown("---")

        # Add new join section
        st.markdown("#### Add Join")

        # Visualization mode toggle
        viz_mode = st.radio(
            "Interface",
            options=["Form", "Visual"],
            horizontal=True,
            help="Form: Standard dropdowns | Visual: Canvas-style interface",
            key=f"{key}_viz_mode"
        )

        if viz_mode == "Form":
            JoinVisualizer._render_form_builder(sources, key)
        else:
            JoinVisualizer._render_visual_builder(sources, key)

        return joins

    @staticmethod
    def _render_form_builder(sources: List[Dict[str, str]], key: str):
        """Render form-based join builder.

        Args:
            sources: List of source dictionaries
            key: Component key
        """
        source_names = [s['name'] for s in sources]

        with st.form(key=f"{key}_add_form"):
            col1, col2 = st.columns(2)

            with col1:
                left_table = st.selectbox(
                    "Left Table *",
                    options=source_names,
                    index=None,
                    placeholder="Choose left table...",
                    key=f"{key}_left_table"
                )

                join_type = st.selectbox(
                    "Join Type",
                    options=["inner", "left", "right", "full"],
                    index=0,
                    key=f"{key}_join_type"
                )

            with col2:
                right_table = st.selectbox(
                    "Right Table *",
                    options=source_names,
                    index=None,
                    placeholder="Choose right table...",
                    key=f"{key}_right_table"
                )

            st.markdown("**Join Keys**")

            col1, col2 = st.columns(2)

            with col1:
                left_key = st.text_input(
                    "Left Key Column *",
                    placeholder="e.g., customer_id",
                    key=f"{key}_left_key"
                )

            with col2:
                right_key = st.text_input(
                    "Right Key Column *",
                    placeholder="e.g., id",
                    key=f"{key}_right_key"
                )

            # Validation
            if left_table and right_table and left_table == right_table:
                st.warning("⚠️ Left and right tables should be different")

            # Preview
            if left_table and right_table and left_key and right_key:
                st.info(
                    f"📝 This will join: `{left_table}.{left_key}` "
                    f"with `{right_table}.{right_key}` "
                    f"using **{join_type.upper()}** join"
                )

            # Submit
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("➕ Add Join", use_container_width=True)
            with col2:
                if st.form_submit_button("Cancel"):
                    st.rerun()

            if submitted:
                if not left_table or not right_table:
                    st.error("Both left and right tables are required")
                elif not left_key or not right_key:
                    st.error("Both join keys are required")
                elif left_table == right_table:
                    st.error("Left and right tables must be different")
                else:
                    new_join = Join(
                        left_table=left_table,
                        right_table=right_table,
                        left_key=left_key,
                        right_key=right_key,
                        join_type=join_type
                    )

                    joins = st.session_state[f"{key}_joins"]

                    # Check for duplicates
                    if any(
                        j.left_table == new_join.left_table
                        and j.right_table == new_join.right_table
                        and j.left_key == new_join.left_key
                        and j.right_key == new_join.right_key
                        for j in joins
                    ):
                        st.warning("⚠️ This join already exists")
                    else:
                        joins.append(new_join)
                        st.session_state[f"{key}_joins"] = joins
                        st.success(f"✅ Join added!")
                        st.rerun()

    @staticmethod
    def _render_visual_builder(sources: List[Dict[str, str]], key: str):
        """Render visual canvas-style join builder.

        Args:
            sources: List of source dictionaries
            key: Component key
        """
        st.info("🎨 Visual join builder - drag and drop interface (Simplified version)")

        # Display tables as boxes
        source_names = [s['name'] for s in sources]

        # Table selection
        st.markdown("**Select Tables to Join:**")

        col1, col2 = st.columns(2)

        with col1:
            left_table = st.selectbox(
                "Left Table",
                options=source_names,
                index=None,
                key=f"{key}_vis_left"
            )

        with col2:
            right_table = st.selectbox(
                "Right Table",
                options=source_names,
                index=None,
                key=f"{key}_vis_right"
            )

        if left_table and right_table:
            # Visual representation
            st.markdown("---")

            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                st.info(f"**{left_table}**")
                left_key = st.text_input(
                    "Join Key",
                    placeholder="column name",
                    key=f"{key}_vis_left_key"
                )

            with col2:
                # Join type in center
                join_type = st.selectbox(
                    "Join",
                    options=["inner", "left", "right", "full"],
                    key=f"{key}_vis_type"
                )
                st.markdown(f"<div style='text-align: center; font-size: 24px;'>↔️</div>",
                          unsafe_allow_html=True)

            with col3:
                st.info(f"**{right_table}**")
                right_key = st.text_input(
                    "Join Key",
                    placeholder="column name",
                    key=f"{key}_vis_right_key"
                )

            if left_key and right_key:
                if st.button("➕ Add Join", key=f"{key}_vis_add", use_container_width=True):
                    new_join = Join(
                        left_table=left_table,
                        right_table=right_table,
                        left_key=left_key,
                        right_key=right_key,
                        join_type=join_type
                    )

                    joins = st.session_state[f"{key}_joins"]
                    joins.append(new_join)
                    st.session_state[f"{key}_joins"] = joins
                    st.success(f"✅ Join added!")
                    st.rerun()

    @staticmethod
    def _edit_join(index: int, key: str):
        """Edit an existing join.

        Args:
            index: Index of join to edit
            key: Component key
        """
        # Store editing state
        st.session_state[f"{key}_editing"] = index
        st.rerun()

    @staticmethod
    def render_simple(
        sources: List[Dict[str, str]],
        key: str = "simple_join"
    ) -> List[Join]:
        """Render simplified join builder for basic use cases.

        Args:
            sources: List of source dictionaries
            key: Component key

        Returns:
            List of Join objects
        """
        st.markdown("**Configure Joins** (Optional)")

        if len(sources) < 2:
            return []

        source_names = [s['name'] for s in sources]

        with st.expander("Add Join"):
            col1, col2 = st.columns(2)

            with col1:
                left = st.selectbox("Left table", source_names, key=f"{key}_left")
                left_key = st.text_input("Left key", key=f"{key}_left_key")

            with col2:
                right = st.selectbox("Right table", source_names, key=f"{key}_right")
                right_key = st.text_input("Right key", key=f"{key}_right_key")

            join_type = st.selectbox(
                "Join type",
                ["inner", "left", "right", "full"],
                key=f"{key}_type"
            )

            if st.button("Add Join", key=f"{key}_add"):
                if left and right and left_key and right_key and left != right:
                    return [Join(
                        left_table=left,
                        right_table=right,
                        left_key=left_key,
                        right_key=right_key,
                        join_type=join_type
                    )]

        return []
