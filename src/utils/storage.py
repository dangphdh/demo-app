"""Storage utility for saving and loading metric views."""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st
from src.models import MetricView


class MetricViewStorage:
    """Storage manager for metric views."""

    # Storage directory
    STORAGE_DIR = "saved_metric_views"

    @staticmethod
    def get_storage_dir() -> str:
        """Get storage directory path, creating if needed.

        Returns:
            Path to storage directory
        """
        if not os.path.exists(MetricViewStorage.STORAGE_DIR):
            os.makedirs(MetricViewStorage.STORAGE_DIR)
        return MetricViewStorage.STORAGE_DIR

    @staticmethod
    def save(metric_view: MetricView, filename: Optional[str] = None) -> str:
        """Save a metric view to storage.

        Args:
            metric_view: MetricView to save
            filename: Optional filename (auto-generated if not provided)

        Returns:
            Path to saved file
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{metric_view.name}_{timestamp}.json"

        # Ensure .json extension
        if not filename.endswith(".json"):
            filename += ".json"

        # Build filepath
        filepath = os.path.join(MetricViewStorage.get_storage_dir(), filename)

        # Prepare data for serialization
        data = {
            "metric_view": metric_view.model_dump(),
            "metadata": {
                "saved_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        }

        # Write to file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath

    @staticmethod
    def load(filename: str) -> Optional[MetricView]:
        """Load a metric view from storage.

        Args:
            filename: Name of file to load

        Returns:
            MetricView object or None if error
        """
        filepath = os.path.join(MetricViewStorage.get_storage_dir(), filename)

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Extract metric view data
            mv_data = data.get("metric_view", {})
            metadata = data.get("metadata", {})

            return MetricView(**mv_data)

        except Exception as e:
            st.error(f"Error loading metric view: {str(e)}")
            return None

    @staticmethod
    def list_saved() -> List[Dict[str, Any]]:
        """List all saved metric views.

        Returns:
            List of dicts with 'filename', 'name', 'saved_at' keys
        """
        storage_dir = MetricViewStorage.get_storage_dir()

        if not os.path.exists(storage_dir):
            return []

        saved_views = []

        for filename in os.listdir(storage_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(storage_dir, filename)

                try:
                    # Read metadata
                    with open(filepath, 'r') as f:
                        data = json.load(f)

                    mv_data = data.get("metric_view", {})
                    metadata = data.get("metadata", {})

                    saved_views.append({
                        "filename": filename,
                        "name": mv_data.get("name", "Unknown"),
                        "description": mv_data.get("description", ""),
                        "saved_at": metadata.get("saved_at", ""),
                        "catalog": mv_data.get("catalog", ""),
                        "schema": mv_data.get("schema", ""),
                        "sources_count": len(mv_data.get("sources", [])),
                        "dimensions_count": len(mv_data.get("dimensions", [])),
                        "measures_count": len(mv_data.get("measures", []))
                    })

                except Exception as e:
                    # Skip files that can't be read
                    continue

        # Sort by saved_at (newest first)
        saved_views.sort(
            key=lambda x: x.get("saved_at", ""),
            reverse=True
        )

        return saved_views

    @staticmethod
    def delete(filename: str) -> bool:
        """Delete a saved metric view.

        Args:
            filename: Name of file to delete

        Returns:
            True if deleted, False otherwise
        """
        filepath = os.path.join(MetricViewStorage.get_storage_dir(), filename)

        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception:
                return False

        return False

    @staticmethod
    def export_yaml(metric_view: MetricView) -> str:
        """Export metric view as YAML string.

        Args:
            metric_view: MetricView to export

        Returns:
            YAML string
        """
        from src.services import YAMLGenerator
        return YAMLGenerator.generate(metric_view)

    @staticmethod
    def import_from_yaml(yaml_content: str) -> Optional[MetricView]:
        """Import metric view from YAML string.

        Args:
            yaml_content: YAML string

        Returns:
            MetricView object or None if error
        """
        import yaml

        try:
            data = yaml.safe_load(yaml_content)

            # Transform Databricks YAML format to Pydantic model format
            data = MetricViewStorage._convert_yaml_to_model_format(data)

            # Convert to MetricView
            return MetricView(**data)

        except Exception as e:
            st.error(f"Error importing YAML: {str(e)}")
            return None

    @staticmethod
    def _convert_yaml_to_model_format(data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Databricks YAML format to Pydantic model format.

        Args:
            data: Raw YAML data dictionary

        Returns:
            Transformed data dictionary matching Pydantic model structure
        """
        # Convert sources from Databricks format to model format
        if "sources" in data:
            converted_sources = []
            for source in data["sources"]:
                converted_source = {"name": source["name"]}

                # Determine type and extract fields
                if "table" in source:
                    converted_source["type"] = "table"
                    table_data = source["table"]
                    converted_source["catalog"] = table_data["catalog"]
                    converted_source["schema"] = table_data["schema"]
                    converted_source["table"] = table_data["name"]
                elif "view" in source:
                    converted_source["type"] = "view"
                    view_data = source["view"]
                    converted_source["catalog"] = view_data["catalog"]
                    converted_source["schema"] = view_data["schema"]
                    converted_source["table"] = view_data["name"]
                elif "query" in source:
                    converted_source["type"] = "query"
                    query_data = source["query"]
                    converted_source["catalog"] = query_data["catalog"]
                    converted_source["schema"] = query_data["schema"]
                    converted_source["query"] = query_data["query"]
                else:
                    # No type specified, default to table
                    converted_source["type"] = "table"

                converted_sources.append(converted_source)

            data["sources"] = converted_sources

        # Convert dimensions from Databricks format to model format
        if "dimensions" in data:
            converted_dimensions = []
            for dimension in data["dimensions"]:
                converted_dim = {"name": dimension["name"]}

                # Determine type
                if "expression" in dimension:
                    converted_dim["type"] = "custom"
                    converted_dim["expression"] = dimension["expression"]
                elif "column" in dimension:
                    converted_dim["type"] = "column"
                    converted_dim["column"] = dimension["column"]
                else:
                    # Default to column type
                    converted_dim["type"] = "column"

                # Copy optional fields
                if "description" in dimension:
                    converted_dim["description"] = dimension["description"]
                if "type" in dimension and isinstance(dimension["type"], str):
                    # Data type field (not the dimension type)
                    converted_dim["data_type"] = dimension["type"]

                converted_dimensions.append(converted_dim)

            data["dimensions"] = converted_dimensions

        return data


class SessionManager:
    """Manager for auto-save and session recovery."""

    AUTOSAVE_KEY = "autosave_metric_view"
    AUTOSAVE_TIMESTAMP = "autosave_timestamp"

    @staticmethod
    def autosave(metric_view: MetricView):
        """Auto-save metric view to session state.

        Args:
            metric_view: MetricView to save
        """
        try:
            st.session_state[SessionManager.AUTOSAVE_KEY] = (
                metric_view.model_dump_json()
            )
            st.session_state[SessionManager.AUTOSAVE_TIMESTAMP] = (
                datetime.now().isoformat()
            )
        except Exception as e:
            # Silent fail for autosave
            pass

    @staticmethod
    def get_autosave() -> Optional[MetricView]:
        """Get auto-saved metric view from session.

        Returns:
            MetricView object or None
        """
        autosave_json = st.session_state.get(SessionManager.AUTOSAVE_KEY)

        if autosave_json:
            try:
                data = json.loads(autosave_json)
                return MetricView(**data)
            except Exception:
                return None

        return None

    @staticmethod
    def has_autosave() -> bool:
        """Check if there's an auto-saved metric view.

        Returns:
            True if autosave exists
        """
        return SessionManager.AUTOSAVE_KEY in st.session_state

    @staticmethod
    def clear_autosave():
        """Clear auto-saved metric view."""
        if SessionManager.AUTOSAVE_KEY in st.session_state:
            del st.session_state[SessionManager.AUTOSAVE_KEY]
        if SessionManager.AUTOSAVE_TIMESTAMP in st.session_state:
            del st.session_state[SessionManager.AUTOSAVE_TIMESTAMP]

    @staticmethod
    def get_autosave_timestamp() -> Optional[str]:
        """Get timestamp of last autosave.

        Returns:
            Timestamp string or None
        """
        return st.session_state.get(SessionManager.AUTOSAVE_TIMESTAMP)

    @staticmethod
    def render_autosave_banner():
        """Render autosave recovery banner if autosave exists."""
        if SessionManager.has_autosave():
            timestamp = SessionManager.get_autosave_timestamp()

            st.info(f"""
            💾 **Auto-saved work found** (saved at {timestamp})

            Would you like to restore your previous work?
            """)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔄 Restore", key="autosave_restore"):
                    metric_view = SessionManager.get_autosave()
                    if metric_view:
                        st.session_state.current_metric_view = metric_view
                        st.success("✅ Work restored!")
                        st.rerun()

            with col2:
                if st.button("🗑️ Discard", key="autosave_discard"):
                    SessionManager.clear_autosave()
                    st.success("Auto-saved work discarded")
                    st.rerun()
