"""Smoke tests for UI redesign.

Tests that the theme system loads and components render.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_theme_module_exists():
    """Test that theme module can be imported."""
    from ui import theme
    assert hasattr(theme, 'COLORS')
    assert hasattr(theme, 'SPACING')
    assert hasattr(theme, 'Typography')
    assert 'primary' in theme.COLORS
    assert 'md' in theme.SPACING
    print("✓ Theme module loads correctly")

def test_components_module_exists():
    """Test that components module can be imported."""
    from ui import components
    assert hasattr(components, 'card')
    assert hasattr(components, 'status_badge')
    assert hasattr(components, 'page_header')
    print("✓ Components module loads correctly")

def test_css_generation():
    """Test that CSS can be generated."""
    from ui.theme import get_custom_css
    css = get_custom_css()
    assert isinstance(css, str)
    assert len(css) > 0
    assert '.tech-card' in css
    assert 'background:' in css
    print("✓ CSS generation works")

def test_color_constants():
    """Test that color constants are defined."""
    from ui.theme import COLORS
    assert COLORS['primary'] == '#2563eb'
    assert COLORS['success'] == '#10b981'
    assert COLORS['warning'] == '#f59e0b'
    assert COLORS['error'] == '#ef4444'
    print("✓ Color constants are correct")

def main():
    print("=" * 60)
    print("UI Redesign Smoke Tests")
    print("=" * 60)
    print()

    try:
        test_theme_module_exists()
        test_components_module_exists()
        test_css_generation()
        test_color_constants()

        print()
        print("✅ All UI smoke tests passed!")
        return 0
    except Exception as e:
        print()
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
