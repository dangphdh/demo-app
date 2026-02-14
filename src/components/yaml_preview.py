"""YAML Preview component for displaying generated Metric View YAML."""

import streamlit as st
from typing import Optional
from src.models import MetricView
from src.services import YAMLGenerator


class YAMLPreview:
    """Component for previewing generated YAML."""

    @staticmethod
    def render(
        metric_view: Optional[MetricView],
        key: str = "yaml_preview",
        show_download: bool = True
    ) -> str:
        """Render the YAML preview panel.

        Args:
            metric_view: MetricView model instance (None if not ready)
            key: Unique key for this component instance
            show_download: Whether to show download button

        Returns:
            Generated YAML string
        """
        # YAML Preview
        st.markdown(f"<div class='tech-card-header'>YAML Preview</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tech-code-preview'>", unsafe_allow_html=True)

        if not metric_view:
            st.info("""
            👆 Complete the wizard steps to generate YAML.

            Your metric view YAML will appear here as you build:
            - Select sources
            - Configure joins
            - Define dimensions
            - Define measures
            """)
            st.markdown("</div>", unsafe_allow_html=True)
            return ""

        # Generate YAML
        try:
            yaml_content = YAMLGenerator.generate(metric_view)

            # Display YAML with syntax highlighting
            st.code(yaml_content, language="yaml", line_numbers=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Show download button
            if show_download:
                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label="Download YAML",
                        data=yaml_content,
                        file_name=f"{metric_view.name}_metric_view.yaml",
                        mime="text/yaml",
                        use_container_width=True
                    )

                with col2:
                    if st.button("Copy to Clipboard", key=f"{key}_copy"):
                        st.clipboard_copy(yaml_content)
                        st.success("✅ Copied to clipboard!")

            # Show validation button
            if st.button("Validate YAML", key=f"{key}_validate"):
                with st.spinner("Validating..."):
                    YAMLPreview._show_validation(metric_view)

            return yaml_content

        except Exception as e:
            st.error(f"❌ Error generating YAML: {str(e)}")
            return ""

    @staticmethod
    def _show_validation(metric_view: MetricView):
        """Show validation results for the metric view.

        Args:
            metric_view: MetricView to validate
        """
        from src.services import Validator

        errors = Validator.validate_metric_view(metric_view)

        if not errors:
            st.success("✅ No validation errors found!")
            st.info("🎉 Your metric view is ready to deploy!")
        else:
            # Group by severity
            error_count = sum(1 for e in errors if e.severity == "error")
            warning_count = sum(1 for e in errors if e.severity == "warning")

            if error_count > 0:
                st.error(f"❌ Found {error_count} error(s)")
            if warning_count > 0:
                st.warning(f"⚠️ Found {warning_count} warning(s)")

            # Show errors
            with st.expander("View Details", expanded=True):
                for i, error in enumerate(errors):
                    if error.severity == "error":
                        st.error(f"**{error.field}**: {error.message}")
                        if error.suggestion:
                            st.info(f"💡 {error.suggestion}")
                    else:
                        st.warning(f"**{error.field}**: {error.message}")
                        if error.suggestion:
                            st.caption(f"💡 {error.suggestion}")
                    st.markdown("---")

    @staticmethod
    def render_compact(
        metric_view: Optional[MetricView],
        key: str = "yaml_preview_compact"
    ) -> str:
        """Render compact YAML preview for side panel.

        Args:
            metric_view: MetricView model instance
            key: Unique key for this component instance

        Returns:
            Generated YAML string
        """
        if not metric_view:
            st.caption("YAML will appear here...")
            return ""

        try:
            yaml_content = YAMLGenerator.generate(metric_view)

            with st.expander("View Generated YAML", expanded=False):
                st.code(yaml_content, language="yaml", line_numbers=True)

                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label="Download",
                        data=yaml_content,
                        file_name=f"{metric_view.name}_metric_view.yaml",
                        mime="text/yaml",
                        use_container_width=True,
                        key=f"{key}_download"
                    )

                with col2:
                    if st.button("Copy", key=f"{key}_copy"):
                        st.clipboard_copy(yaml_content)
                        st.success("Copied!")

            return yaml_content

        except Exception as e:
            st.error(f"Error: {str(e)}")
            return ""

    @staticmethod
    def render_summary(metric_view: Optional[MetricView]) -> bool:
        """Render a summary of the metric view.

        Args:
            metric_view: MetricView model instance

        Returns:
            True if metric view is valid and complete
        """
        if not metric_view:
            st.info("📝 Complete all steps to see summary")
            return False

        st.markdown("### 📊 Metric View Summary")

        # Basic info
        col1, col2 = st.columns(2)
        with col1:
            st.text(f"**Name:** {metric_view.name}")
        with col2:
            st.text(f"**Location:** {metric_view.catalog}.{metric_view.schema}")

        if metric_view.description:
            st.caption(f"📝 {metric_view.description}")

        st.markdown("---")

        # Sources
        st.markdown("**Sources:**")
        for source in metric_view.sources:
            st.text(f"• {source.name}: `{source.get_full_name()}`")

        # Dimensions
        if metric_view.dimensions:
            st.markdown(f"**Dimensions** ({len(metric_view.dimensions)}):")
            dim_list = ", ".join([f"`{d.name}`" for d in metric_view.dimensions])
            st.text(dim_list)

        # Measures
        if metric_view.measures:
            st.markdown(f"**Measures** ({len(metric_view.measures)}):")
            measure_list = ", ".join([f"`{m.name}`" for m in metric_view.measures])
            st.text(measure_list)

        # Joins
        if metric_view.joins:
            st.markdown(f"**Joins** ({len(metric_view.joins)}):")
            for join in metric_view.joins:
                st.text(
                    f"• {join.left_table}.{join.left_key} "
                    f"←[{join.join_type}]→ "
                    f"{join.right_table}.{join.right_key}"
                )

        st.markdown("---")

        # Validation check
        from src.services import Validator
        errors = Validator.validate_metric_view(metric_view)

        if errors:
            error_count = sum(1 for e in errors if e.severity == "error")
            if error_count > 0:
                st.error(f"⚠️ Has {error_count} validation error(s)")
                return False
            else:
                st.warning("⚠️ Has validation warnings (non-blocking)")
                return True
        else:
            st.success("✅ Ready to deploy!")
            return True
