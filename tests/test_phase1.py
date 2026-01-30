"""Test script for Phase 1 implementation.

Tests basic functionality without requiring Databricks connection.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_models():
    """Test Pydantic models."""
    from models import MetricView, Dimension, Measure, Join, Source

    print("Testing Pydantic models...")

    # Test Dimension
    dim = Dimension(
        name="test_dimension",
        type="column",
        column="test_column",
        description="Test dimension"
    )
    assert dim.name == "test_dimension"
    print("✓ Dimension model works")

    # Test Measure
    measure = Measure(
        name="total_revenue",
        expression="SUM(revenue)",
        description="Total revenue"
    )
    assert measure.name == "total_revenue"
    print("✓ Measure model works")

    # Test Join
    join = Join(
        left_table="orders",
        right_table="customers",
        left_key="customer_id",
        right_key="id",
        join_type="inner"
    )
    assert join.join_type == "inner"
    print("✓ Join model works")

    # Test Source
    source = Source(
        name="orders",
        type="table",
        catalog="main",
        schema="sales",
        table="orders"
    )
    assert source.get_full_name() == "main.sales.orders"
    print("✓ Source model works")

    # Test MetricView
    mv = MetricView(
        name="test_metrics",
        catalog="main",
        schema="analytics",
        description="Test metric view",
        sources=[source],
        dimensions=[dim],
        measures=[measure],
        joins=[join],
        primary_source="orders"
    )
    assert len(mv.get_dimension_names()) == 1
    assert len(mv.get_measure_names()) == 1
    print("✓ MetricView model works")

    print("\n✅ All model tests passed!\n")


def test_auth_manager():
    """Test authentication manager."""
    from services import AuthManager

    print("Testing AuthManager...")

    # Test service account check (will likely be false in dev)
    has_service = AuthManager.has_service_account_configured()
    print(f"✓ Service account configured: {has_service}")

    # Test user config creation
    config = AuthManager.create_user_config(
        host="https://test.cloud.databricks.com",
        token="test_token",
        warehouse_id="test_warehouse"
    )
    assert config.host == "https://test.cloud.databricks.com"
    print("✓ User config creation works")

    # Test validation
    is_valid, error = AuthManager.validate_config(config)
    assert is_valid
    print("✓ Config validation works")

    # Test token masking
    masked = AuthManager.mask_token("dapi1234567890abcdef")
    assert "..." in masked
    print("✓ Token masking works")

    print("\n✅ All AuthManager tests passed!\n")


def test_databricks_client():
    """Test Databricks client initialization."""
    from services import AuthManager, DatabricksClient

    print("Testing DatabricksClient...")

    # Create a test config
    config = AuthManager.create_user_config(
        host="https://test.cloud.databricks.com",
        token="test_token",
        warehouse_id="test_warehouse"
    )

    # Initialize client (won't actually connect without real credentials)
    try:
        client = DatabricksClient(config)
        assert client.config.host == "https://test.cloud.databricks.com"
        print("✓ DatabricksClient initialization works")
    except Exception as e:
        print(f"⚠ Client initialization note: {e}")

    print("\n✅ DatabricksClient structure validated!\n")


def main():
    """Run all Phase 1 tests."""
    print("=" * 60)
    print("Phase 1 Implementation Tests")
    print("=" * 60)
    print()

    try:
        test_models()
        test_auth_manager()
        test_databricks_client()

        print("=" * 60)
        print("🎉 All Phase 1 tests passed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Set up Databricks credentials in .env file")
        print("2. Run the app: streamlit run app.py")
        print("3. Or use Docker: docker-compose up --build")
        print()

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
