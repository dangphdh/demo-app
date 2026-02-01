"""Measure Builder component for creating and editing measures."""

import streamlit as st
from typing import List, Dict, Any, Optional
from src.models import Measure


class MeasureBuilder:
    """Component for building measures (simple and advanced)."""

    @staticmethod
    def render(
        available_columns: List[Dict[str, Any]],
        existing_measures: List[Measure],
        key: str = "measure_builder"
    ) -> List[Measure]:
        """Render the measure builder UI.

        Args:
            available_columns: List of available column dictionaries
            existing_measures: List of existing Measure objects
            key: Unique key for this component instance

        Returns:
            Updated list of Measure objects
        """
        st.subheader("📈 Define Measures")

        # Help text
        with st.expander("ℹ️ What is a Measure?"):
            st.markdown("""
            A **measure** is a value that summarizes business activity, typically using
            an aggregate function such as `SUM()`, `COUNT()`, `AVG()`, `MIN()`, or `MAX()`.

            **Examples:**
            - `total_revenue = SUM(order_amount)`
            - `order_count = COUNT(*)`
            - `avg_order_value = AVG(order_amount)`
            - `unique_customers = COUNT(DISTINCT customer_id)`
            - `revenue_per_customer = SUM(revenue) / COUNT(DISTINCT customer_id)`
            """)

        # Initialize session state
        if f"{key}_measures" not in st.session_state:
            st.session_state[f"{key}_measures"] = existing_measures.copy()

        if f"{key}_mode" not in st.session_state:
            st.session_state[f"{key}_mode"] = "simple"

        measures = st.session_state[f"{key}_measures"]

        # Show existing measures
        if measures:
            st.markdown("**Current Measures:**")
            for i, measure in enumerate(measures):
                with st.container():
                    col1, col2, col3 = st.columns([4, 1, 1])

                    with col1:
                        st.text(f"**{measure.name}**")
                        st.code(measure.expression, language="sql")
                        if measure.description:
                            st.caption(measure.description)

                    with col2:
                        if st.button("✏️", key=f"{key}_edit_{i}"):
                            MeasureBuilder._edit_measure(i, key)

                    with col3:
                        if st.button("🗑️", key=f"{key}_delete_{i}"):
                            measures.pop(i)
                            st.session_state[f"{key}_measures"] = measures
                            st.rerun()

                    st.markdown("---")

        # Mode toggle
        mode = st.radio(
            "Builder Mode",
            options=["Simple", "Advanced"],
            horizontal=True,
            index=0 if st.session_state.get(f"{key}_mode", "Simple") == "Simple" else 1,
            key=f"{key}_mode_select",
            help="Simple: Quick measure presets | Advanced: Custom SQL expressions"
        )

        if mode != st.session_state[f"{key}_mode"]:
            st.session_state[f"{key}_mode"] = mode
            st.rerun()

        if mode == "simple":
            MeasureBuilder._render_simple_builder(available_columns, key)
        else:
            MeasureBuilder._render_advanced_builder(key)

        return measures

    @staticmethod
    def _render_simple_builder(available_columns: List[Dict[str, Any]], key: str):
        """Render simple measure builder with presets.

        Args:
            available_columns: List of available column dictionaries
            key: Component key
        """
        st.markdown("#### Add Measure (Simple Mode)")

        with st.form(key=f"{key}_simple_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Measure type
                measure_type = st.selectbox(
                    "Measure Type *",
                    options=[
                        "Sum",
                        "Count",
                        "Average",
                        "Min",
                        "Max",
                        "Count Distinct"
                    ],
                    key=f"{key}_simple_type"
                )

                # Measure name
                name = st.text_input(
                    "Measure Name *",
                    placeholder="e.g., total_revenue",
                    key=f"{key}_simple_name"
                )

            with col2:
                # Column selection
                column_names = [col['name'] for col in available_columns]
                column = st.selectbox(
                    "Select Column *",
                    options=column_names,
                    index=None,
                    placeholder="Choose a column...",
                    key=f"{key}_simple_column"
                )

                # Description
                description = st.text_input(
                    "Description",
                    placeholder="What does this measure calculate?",
                    key=f"{key}_simple_description"
                )

            # Show preview expression
            if measure_type and column:
                expression = MeasureBuilder._build_simple_expression(
                    measure_type, column
                )
                st.info(f"📝 Expression preview: `{expression}`")

            # Submit
            submitted = st.form_submit_button("➕ Add Measure", use_container_width=True)

            if submitted:
                if not name:
                    st.error("Measure name is required")
                elif not column:
                    st.error("Please select a column")
                else:
                    expression = MeasureBuilder._build_simple_expression(
                        measure_type, column
                    )
                    new_measure = Measure(
                        name=name.strip(),
                        expression=expression,
                        description=description.strip() if description else ""
                    )

                    measures = st.session_state[f"{key}_measures"]
                    if any(m.name == new_measure.name for m in measures):
                        st.error(f"Measure '{name}' already exists")
                    else:
                        measures.append(new_measure)
                        st.session_state[f"{key}_measures"] = measures
                        st.success(f"✅ Measure '{name}' added!")
                        st.rerun()

    @staticmethod
    def _render_advanced_builder(key: str):
        """Render advanced measure builder with custom expressions.

        Args:
            key: Component key
        """
        st.markdown("#### Add Measure (Advanced Mode)")

        with st.form(key=f"{key}_advanced_form"):
            name = st.text_input(
                "Measure Name *",
                placeholder="e.g., revenue_per_customer",
                key=f"{key}_adv_name"
            )

            expression = st.text_area(
                "SQL Expression *",
                placeholder="e.g., SUM(revenue) / COUNT(DISTINCT customer_id)",
                help="Enter any valid SQL aggregate expression",
                key=f"{key}_adv_expression"
            )

            description = st.text_input(
                "Description",
                placeholder="What does this measure calculate?",
                key=f"{key}_adv_description"
            )

            # Show expression examples
            with st.expander("💡 Expression Examples"):
                st.markdown("""
                **Basic Aggregates:**
                ```
                SUM(column_name)
                COUNT(*)
                AVG(column_name)
                MIN(column_name)
                MAX(column_name)
                ```

                **Distinct Counts:**
                ```
                COUNT(DISTINCT customer_id)
                COUNT(DISTINCT CASE WHEN status = 'active' THEN user_id END)
                ```

                **Ratios and Division:**
                ```
                SUM(revenue) / COUNT(DISTINCT customer_id)
                SUM(profit) / NULLIF(SUM(revenue), 0)
                ```

                **Conditional Aggregates:**
                ```
                SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END)
                COUNT(DISTINCT CASE WHEN revenue > 1000 THEN customer_id END)
                ```

                **Multi-Column Expressions:**
                ```
                SUM(quantity * unit_price)
                AVG(total_amount - discount_amount)
                ```
                """)

            # Submit
            submitted = st.form_submit_button("➕ Add Measure", use_container_width=True)

            if submitted:
                if not name:
                    st.error("Measure name is required")
                elif not expression:
                    st.error("SQL expression is required")
                else:
                    new_measure = Measure(
                        name=name.strip(),
                        expression=expression.strip(),
                        description=description.strip() if description else ""
                    )

                    measures = st.session_state[f"{key}_measures"]
                    if any(m.name == new_measure.name for m in measures):
                        st.error(f"Measure '{name}' already exists")
                    else:
                        measures.append(new_measure)
                        st.session_state[f"{key}_measures"] = measures
                        st.success(f"✅ Measure '{name}' added!")
                        st.rerun()

    @staticmethod
    def _build_simple_expression(measure_type: str, column: str) -> str:
        """Build SQL expression from simple measure type.

        Args:
            measure_type: Type of measure (Sum, Count, etc.)
            column: Column name

        Returns:
            SQL expression string
        """
        type_map = {
            "Sum": f"SUM({column})",
            "Count": f"COUNT({column})",
            "Average": f"AVG({column})",
            "Min": f"MIN({column})",
            "Max": f"MAX({column})",
            "Count Distinct": f"COUNT(DISTINCT {column})"
        }

        return type_map.get(measure_type, f"SUM({column})")

    @staticmethod
    def _edit_measure(index: int, key: str):
        """Edit an existing measure.

        Args:
            index: Index of measure to edit
            key: Component key
        """
        # Store editing state
        st.session_state[f"{key}_editing"] = index
        st.rerun()
