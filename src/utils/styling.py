"""Enhanced styling utilities for the application."""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS for professional styling."""
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #1f77b4 0%, #17becf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #1f77b4;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Success boxes */
    .success-box {
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffed 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #22c55e;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Warning boxes */
    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #f59e0b;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Error boxes */
    .error-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #ef4444;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }

    /* Feature card */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }

    /* Step indicator */
    .step-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1f77b4 0%, #17becf 100%);
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 0 auto 0.5rem;
    }

    .step-indicator.active {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    }

    .step-indicator.completed {
        background: linear-gradient(135deg, #64748b 0%, #475569 100%);
    }

    /* Metric view summary */
    .mv-summary {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #e2e8f0;
    }

    /* Button enhancements */
    .stButton > button {
        border-radius: 0.5rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
    }

    /* Code blocks */
    .code-block {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
        margin: 1rem 0;
    }

    /* Template cards */
    .template-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 1rem;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        text-align: center;
    }

    .template-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 8px 20px rgba(31, 119, 180, 0.15);
        transform: translateY(-2px);
    }

    /* Autosave banner */
    .autosave-banner {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin-bottom: 1rem;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1f77b4 0%, #17becf 100%);
    }

    /* Sidebar enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, #1f77b4 0%, #1e5a7e 100%);
    }

    .css-1d391kg .css-17eq0hr {
        color: white;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 0.5rem;
        padding: 0.75rem;
        border: 1px solid #e2e8f0;
        font-weight: 600;
    }

    /* Metric stats */
    .metric-stat {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        border: 2px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .metric-stat .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
    }

    .metric-stat .label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Validation errors */
    .validation-error {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin: 0.5rem 0;
    }

    .validation-warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin: 0.5rem 0;
    }

    /* Helper text */
    .helper-text {
        font-size: 0.85rem;
        color: #64748b;
        font-style: italic;
        margin-top: 0.25rem;
    }

    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_metric_stat(label: str, value: int, icon: str = ""):
    """Render a metric statistic card.

    Args:
        label: Stat label
        value: Stat value
        icon: Optional icon
    """
    icon_html = f"<div style='font-size: 2rem;'>{icon}</div>" if icon else ""

    st.markdown(f"""
    <div class="metric-stat">
        {icon_html}
        <div class="value">{value}</div>
        <div class="label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_info_box(title: str, content: str, icon: str = "ℹ️"):
    """Render an info box.

    Args:
        title: Box title
        content: Box content
        icon: Optional icon
    """
    st.markdown(f"""
    <div class="info-box">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_success_box(title: str, content: str, icon: str = "✅"):
    """Render a success box.

    Args:
        title: Box title
        content: Box content
        icon: Optional icon
    """
    st.markdown(f"""
    <div class="success-box">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_warning_box(title: str, content: str, icon: str = "⚠️"):
    """Render a warning box.

    Args:
        title: Box title
        content: Box content
        icon: Optional icon
    """
    st.markdown(f"""
    <div class="warning-box">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_error_box(title: str, content: str, icon: str = "❌"):
    """Render an error box.

    Args:
        title: Box title
        content: Box content
        icon: Optional icon
    """
    st.markdown(f"""
    <div class="error-box">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str):
    """Render a section header.

    Args:
        title: Header text
    """
    st.markdown(f"""
    <div class="section-header">
        {title}
    </div>
    """, unsafe_allow_html=True)


def render_custom_divider():
    """Render a custom divider."""
    st.markdown("""
    <div class="custom-divider"></div>
    """, unsafe_allow_html=True)
