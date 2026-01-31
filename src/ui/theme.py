"""Theme system for professional analytics platform styling."""

import streamlit as st

# Color Palette - Corporate Analytics
COLORS = {
    # Backgrounds
    'background': '#ffffff',
    'background_secondary': '#f8fafc',
    'background_tertiary': '#f1f5f9',

    # Text
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_muted': '#94a3b8',

    # Primary Colors
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',

    # Status Colors
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'pending': '#94a3b8',

    # Borders
    'border': '#e2e8f0',
}

# Spacing System (4px base unit)
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
    'xxl': '48px',
}

class Typography:
    """Typography scale."""
    H1 = '28px'
    H2 = '24px'
    H3 = '20px'
    BODY = '16px'
    SMALL = '14px'
    XSMALL = '12px'


def get_custom_css() -> str:
    """Generate custom CSS for the entire application.

    Returns:
        str: CSS stylesheet as string
    """
    return f"""
    <style>
    /* Global Styles */
    .main .block-container {{
        padding-top: {SPACING['lg']};
        padding-bottom: {SPACING['lg']};
        padding-left: {SPACING['lg']};
        padding-right: {SPACING['lg']};
        max-width: 1400px;
    }}

    /* Typography */
    h1 {{
        font-size: {Typography.H1};
        font-weight: 600;
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['sm']};
        line-height: 1.2;
    }}

    h2 {{
        font-size: {Typography.H2};
        font-weight: 600;
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['md']};
        line-height: 1.2;
    }}

    h3 {{
        font-size: {Typography.H3};
        font-weight: 600;
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['sm']};
        line-height: 1.2;
    }}

    p, span, div {{
        font-size: {Typography.BODY};
        color: {COLORS['text_secondary']};
        line-height: 1.5;
    }}

    /* Card Component */
    .tech-card {{
        background: {COLORS['background']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: {SPACING['md']};
        margin-bottom: {SPACING['md']};
    }}

    .tech-card-header {{
        background: {COLORS['background_secondary']};
        border-bottom: 1px solid {COLORS['border']};
        padding: {SPACING['sm']} {SPACING['md']};
        font-size: 18px;
        font-weight: 600;
        color: {COLORS['text_primary']};
        margin: -{SPACING['md']} -{SPACING['md']} {SPACING['md']} -{SPACING['md']};
    }}

    /* Status Badge */
    .tech-status-badge {{
        display: inline-flex;
        align-items: center;
        gap: {SPACING['xs']};
        font-size: {Typography.SMALL};
    }}

    .tech-status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }}

    .tech-status-dot.success {{
        background: {COLORS['success']};
    }}

    .tech-status-dot.warning {{
        background: {COLORS['warning']};
    }}

    .tech-status-dot.error {{
        background: {COLORS['error']};
    }}

    .tech-status-dot.pending {{
        background: {COLORS['pending']};
    }}

    /* Form Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        border: 1px solid {COLORS['border']} !important;
        border-radius: 4px;
        background: {COLORS['background']};
        color: {COLORS['text_primary']};
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: {COLORS['primary']} !important;
        outline: none;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 4px;
        height: 40px;
        padding: 0 {SPACING['md']};
        font-weight: 500;
        transition: none;
    }}

    .stButton > button[kind="primary"] {{
        background: {COLORS['primary']};
        color: white;
        border: none;
    }}

    .stButton > button[kind="primary"]:hover {{
        background: {COLORS['primary_hover']};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {COLORS['background']};
    }}

    .sidebar-title {{
        font-size: {Typography.H2};
        font-weight: 600;
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['md']};
    }}

    /* Code/YAML Preview */
    .tech-code-preview {{
        background: {COLORS['background_secondary']};
        border-radius: 4px;
        padding: {SPACING['md']};
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
        font-size: {Typography.SMALL};
        overflow-x: auto;
    }}

    /* Remove default Streamlit styling */
    .stApp {{}}

    /* Progress indicator for wizard */
    .tech-progress-bar {{
        display: flex;
        gap: {SPACING['sm']};
        margin-bottom: {SPACING['lg']};
    }}

    .tech-progress-step {{
        flex: 1;
        height: 4px;
        background: {COLORS['border']};
        border-radius: 2px;
    }}

    .tech-progress-step.active {{
        background: {COLORS['primary']};
    }}

    .tech-progress-step.completed {{
        background: {COLORS['success']};
    }}
    </style>
    """


def inject_theme():
    """Inject the custom CSS into the Streamlit app."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)
