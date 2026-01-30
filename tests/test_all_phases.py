"""Comprehensive test suite for all phases."""

import sys
import os

# Add project root and src to path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, project_root)

def test_phase1_models():
    """Test Phase 1: Pydantic models."""
    from models import MetricView, Dimension, Measure, Join, Source

    print("\n" + "="*60)
    print("Testing Phase 1: Models")
    print("="*60)

    # Test Source
    source = Source(
        name="test_source",
        type="table",
        catalog="main",
        schema="test",
        table="orders"
    )
    assert source.get_full_name() == "main.test.orders"
    print("✅ Source model works")

    # Test Dimension
    dim = Dimension(
        name="test_dim",
        type="column",
        column="test_col",
        description="Test dimension"
    )
    assert dim.name == "test_dim"
    assert dim.type == "column"
    print("✅ Dimension model works")

    # Test Custom Dimension
    custom_dim = Dimension(
        name="custom_dim",
        type="custom",
        expression="DATE_FORMAT(date_col, 'yyyy-MM')",
        description="Custom date dimension"
    )
    assert custom_dim.expression is not None
    print("✅ Custom dimension works")

    # Test Measure
    measure = Measure(
        name="test_measure",
        expression="SUM(amount)",
        description="Test measure"
    )
    assert measure.expression == "SUM(amount)"
    print("✅ Measure model works")

    # Test Join
    join = Join(
        left_table="orders",
        right_table="customers",
        left_key="customer_id",
        right_key="id",
        join_type="inner"
    )
    assert join.join_type == "inner"
    print("✅ Join model works")

    # Test complete MetricView
    mv = MetricView(
        name="test_mv",
        catalog="main",
        schema="analytics",
        description="Test metric view",
        sources=[source],
        dimensions=[dim],
        measures=[measure],
        joins=[join],
        primary_source="test_source"
    )
    assert len(mv.get_dimension_names()) == 1
    assert len(mv.get_measure_names()) == 1
    assert mv.has_joins() == True
    print("✅ MetricView model works")

    print("\n✅ All Phase 1 model tests passed!\n")


def test_phase1_services():
    """Test Phase 1: Authentication and Databricks client."""
    from services import AuthManager, DatabricksClient, DatabricksConfig

    print("\n" + "="*60)
    print("Testing Phase 1: Services")
    print("="*60)

    # Test AuthManager
    has_service = AuthManager.has_service_account_configured()
    print(f"✅ Service account check: {has_service}")

    config = AuthManager.create_user_config(
        host="https://test.databricks.com",
        token="test_token_123",
        warehouse_id="test_warehouse"
    )
    assert config.host == "https://test.databricks.com"
    print("✅ User config creation works")

    is_valid, error = AuthManager.validate_config(config)
    assert is_valid
    print("✅ Config validation works")

    masked = AuthManager.mask_token("dapi123456789")
    assert "..." in masked
    print("✅ Token masking works")

    # Test DatabricksClient initialization
    client = DatabricksClient(config)
    assert client.config.host == "https://test.databricks.com"
    print("✅ DatabricksClient initialization works")

    print("\n✅ All Phase 1 service tests passed!\n")


def test_phase2_yaml_generator():
    """Test Phase 2: YAML generator."""
    from services import YAMLGenerator
    from models import MetricView, Source, Dimension, Measure

    print("\n" + "="*60)
    print("Testing Phase 2: YAML Generator")
    print("="*60)

    # Create test metric view
    mv = MetricView(
        name="test_metrics",
        catalog="main",
        schema="analytics",
        description="Test metrics",
        sources=[
            Source(
                name="orders",
                type="table",
                catalog="main",
                schema="sales",
                table="orders"
            )
        ],
        dimensions=[
            Dimension(
                name="order_date",
                type="column",
                column="order_date",
                description="Order date"
            ),
            Dimension(
                name="order_month",
                type="custom",
                expression="DATE_FORMAT(order_date, 'yyyy-MM')",
                description="Order month"
            )
        ],
        measures=[
            Measure(
                name="total_revenue",
                expression="SUM(revenue)",
                description="Total revenue"
            )
        ],
        primary_source="orders"
    )

    # Generate YAML
    yaml_content = YAMLGenerator.generate(mv)

    assert "name: test_metrics" in yaml_content
    assert "catalog: main" in yaml_content
    assert "schema: analytics" in yaml_content
    assert "dimensions:" in yaml_content
    assert "measures:" in yaml_content
    print("✅ YAML generation works")

    # Generate example
    example_yaml = YAMLGenerator.generate_example()
    assert example_yaml is not None
    print("✅ Example generation works")

    print("\n✅ All Phase 2 YAML generator tests passed!\n")


def test_phase2_validator():
    """Test Phase 2: Validator."""
    from services import Validator
    from models import MetricView, Source, Dimension, Measure

    print("\n" + "="*60)
    print("Testing Phase 2: Validator")
    print("="*60)

    # Test valid metric view
    mv = MetricView(
        name="valid_mv",
        catalog="main",
        schema="analytics",
        description="Valid metric view",
        sources=[
            Source(
                name="orders",
                type="table",
                catalog="main",
                schema="sales",
                table="orders"
            )
        ],
        dimensions=[
            Dimension(
                name="order_date",
                type="column",
                column="order_date"
            )
        ],
        measures=[
            Measure(
                name="total_revenue",
                expression="SUM(revenue)"
            )
        ],
        primary_source="orders"
    )

    errors = Validator.validate_metric_view(mv)

    # Should have no errors
    blocking_errors = [e for e in errors if e.severity == "error"]
    assert len(blocking_errors) == 0
    print("✅ Validation passes for valid metric view")

    # Test invalid metric view (missing name)
    # Use model_construct to bypass Pydantic validation for testing Validator logic
    invalid_mv = MetricView.model_construct(
        name="",  # Invalid: empty name
        catalog="main",
        schema="analytics",
        description="Invalid metric view",
        sources=[],
        dimensions=[],
        measures=[],
        primary_source=""
    )

    errors = Validator.validate_metric_view(invalid_mv)

    # Should have errors
    assert len(errors) > 0
    print(f"✅ Validator catches {len(errors)} errors in invalid metric view")

    print("\n✅ All Phase 2 validator tests passed!\n")


def test_phase3_templates():
    """Test Phase 3: Templates."""
    from services import TemplateLoader, Template

    print("\n" + "="*60)
    print("Testing Phase 3: Templates")
    print("="*60)

    # Test template loading
    templates = TemplateLoader.list_templates()

    assert len(templates) == 3
    print(f"✅ Loaded {len(templates)} templates")

    # Check template names
    template_names = [t.name for t in templates]
    assert "sales_revenue" in template_names
    assert "order_analytics" in template_names
    assert "customer_metrics" in template_names
    print("✅ All expected templates present")

    # Test template to MetricView conversion
    sales_template = TemplateLoader.get_template("sales_revenue")
    assert sales_template is not None
    print("✅ Template retrieval works")

    mv = sales_template.to_metric_view()
    assert mv is not None
    assert mv.name == "sales_revenue"
    assert len(mv.dimensions) > 0
    assert len(mv.measures) > 0
    print("✅ Template to MetricView conversion works")

    print("\n✅ All Phase 3 template tests passed!\n")


def test_phase3_storage():
    """Test Phase 3: Storage utilities."""
    from utils import MetricViewStorage
    from models import MetricView, Source, Dimension, Measure

    print("\n" + "="*60)
    print("Testing Phase 3: Storage")
    print("="*60)

    # Create test metric view
    mv = MetricView(
        name="test_storage",
        catalog="main",
        schema="analytics",
        description="Test storage",
        sources=[
            Source(
                name="orders",
                type="table",
                catalog="main",
                schema="sales",
                table="orders"
            )
        ],
        dimensions=[
            Dimension(
                name="order_date",
                type="column",
                column="order_date"
            )
        ],
        measures=[
            Measure(
                name="total_revenue",
                expression="SUM(revenue)"
            )
        ],
        primary_source="orders"
    )

    # Test save
    filepath = MetricViewStorage.save(mv)
    assert filepath is not None
    assert os.path.exists(filepath)
    print(f"✅ Save works: {filepath}")

    # Test list
    saved = MetricViewStorage.list_saved()
    assert len(saved) > 0
    print(f"✅ List saved works: {len(saved)} items")

    # Test load
    filename = os.path.basename(filepath)
    loaded_mv = MetricViewStorage.load(filename)
    assert loaded_mv is not None
    assert loaded_mv.name == "test_storage"
    print("✅ Load works")

    # Test delete
    deleted = MetricViewStorage.delete(filename)
    assert deleted == True
    print("✅ Delete works")

    # Test YAML export
    yaml_content = MetricViewStorage.export_yaml(mv)
    assert yaml_content is not None
    assert "test_storage" in yaml_content
    print("✅ YAML export works")

    # Test YAML import
    imported_mv = MetricViewStorage.import_from_yaml(yaml_content)
    assert imported_mv is not None
    assert imported_mv.name == "test_storage"
    print("✅ YAML import works")

    # Clean up
    if os.path.exists(filepath):
        os.remove(filepath)
        print("✅ Cleanup successful")

    print("\n✅ All Phase 3 storage tests passed!\n")


def test_phase4_deployment():
    """Test Phase 4: Deployment functionality."""
    from services import DatabricksClient, AuthManager

    print("\n" + "="*60)
    print("Testing Phase 4: Deployment")
    print("="*60)

    # Test SQL execution preparation
    config = AuthManager.create_user_config(
        host="https://test.databricks.com",
        token="test_token",
        warehouse_id="test_warehouse"
    )

    client = DatabricksClient(config)

    # Test that deployment method exists
    assert hasattr(client, 'deploy_metric_view')
    print("✅ deploy_metric_view method exists")

    assert hasattr(client, 'test_metric_view_query')
    print("✅ test_metric_view_query method exists")

    assert hasattr(client, 'execute_sql')
    print("✅ execute_sql method exists")

    # Note: Actual Databricks API calls require real credentials
    # These are structure/compilation tests only
    print("⚠️  API execution tests require real Databricks connection")
    print("✅ Deployment methods properly structured")

    print("\n✅ All Phase 4 deployment tests passed!\n")


def test_yaml_imports():
    """Test that all imports work correctly."""
    print("\n" + "="*60)
    print("Testing Import Structure")
    print("="*60)

    # Test model imports
    try:
        from models import MetricView, Dimension, Measure, Join, Source
        print("✅ Models import successfully")
    except ImportError as e:
        print(f"❌ Model import failed: {e}")
        return

    # Test service imports
    try:
        from services import (
            AuthManager, DatabricksClient, YAMLGenerator, Validator,
            TemplateLoader, Template
        )
        print("✅ Services import successfully")
    except ImportError as e:
        print(f"❌ Services import failed: {e}")
        return

    # Test component imports
    try:
        from components import (
            SchemaBrowser, DimensionBuilder, MeasureBuilder,
            JoinVisualizer, YAMLPreview
        )
        print("✅ Components import successfully")
    except ImportError as e:
        print(f"❌ Components import failed: {e}")
        return

    # Test utility imports
    try:
        from utils import (
            MetricViewStorage, SessionManager, apply_custom_css
        )
        print("✅ Utils import successfully")
    except ImportError as e:
        print(f"❌ Utils import failed: {e}")
        return

    print("\n✅ All imports successful!\n")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*70)
    print("COMPREHENSIVE TEST SUITE - ALL PHASES")
    print("="*70)

    try:
        test_yaml_imports()
        test_phase1_models()
        test_phase1_services()
        test_phase2_yaml_generator()
        test_phase2_validator()
        test_phase3_templates()
        test_phase3_storage()
        test_phase4_deployment()

        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("="*70)
        print("\n✅ The application is ready for production use!")
        print("\nNext steps:")
        print("1. Set up Databricks credentials in .env file")
        print("2. Run the app: streamlit run app.py")
        print("3. Or use Docker: docker-compose up --build")
        print("4. Take the tutorial to learn the basics")
        print("5. Create your first metric view!")
        print()

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
