"""Authentication manager for Databricks connections.

Handles two authentication methods:
1. Service account (configured in environment variables)
2. User credentials (stored in session state only)
"""

import os
from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class DatabricksConfig:
    """Databricks connection configuration."""

    host: str
    token: str
    warehouse_id: str
    auth_method: Literal["service_account", "user_credentials"]


class AuthManager:
    """Manages Databricks authentication methods."""

    # Service account credentials (from environment)
    SERVICE_HOST = os.getenv("DATABRICKS_HOST", "")
    SERVICE_TOKEN = os.getenv("DATABRICKS_TOKEN", "")
    SERVICE_WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID", "")

    @staticmethod
    def has_service_account_configured() -> bool:
        """Check if service account credentials are configured."""
        return bool(
            AuthManager.SERVICE_HOST
            and AuthManager.SERVICE_TOKEN
            and AuthManager.SERVICE_WAREHOUSE_ID
        )

    @staticmethod
    def get_service_account_config() -> Optional[DatabricksConfig]:
        """Get service account configuration from environment."""
        if AuthManager.has_service_account_configured():
            return DatabricksConfig(
                host=AuthManager.SERVICE_HOST,
                token=AuthManager.SERVICE_TOKEN,
                warehouse_id=AuthManager.SERVICE_WAREHOUSE_ID,
                auth_method="service_account"
            )
        return None

    @staticmethod
    def create_user_config(
        host: str,
        token: str,
        warehouse_id: str
    ) -> DatabricksConfig:
        """Create user credential configuration."""
        return DatabricksConfig(
            host=host,
            token=token,
            warehouse_id=warehouse_id,
            auth_method="user_credentials"
        )

    @staticmethod
    def validate_config(config: DatabricksConfig) -> tuple[bool, Optional[str]]:
        """Validate a Databricks configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not config.host:
            return False, "Databricks host URL is required"

        if not config.host.startswith(("http://", "https://")):
            return False, "Host must start with http:// or https://"

        if not config.token:
            return False, "Databricks access token is required"

        if not config.warehouse_id:
            return False, "SQL Warehouse ID is required"

        return True, None

    @staticmethod
    def mask_token(token: str) -> str:
        """Mask a token for display purposes."""
        if len(token) <= 10:
            return "*" * len(token)
        return f"{token[:4]}...{token[-4:]}"
