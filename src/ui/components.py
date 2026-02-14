"""Reusable UI components for consistent styling."""

import streamlit as st
from .theme import COLORS, SPACING


def card(title=None, content=None, border_color=None):
    """Render a card component.

    Args:
        title: Optional card title (displays in header bar)
        content: Content to display in card (can be string or st element)
        border_color: Optional border color override

    Returns:
        None (renders to Streamlit)
    """
    border = f"border-color: {border_color};" if border_color else ""

    if title:
        st.markdown(f"""
        <div class="tech-card" style="{border}">
            <div class="tech-card-header">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="tech-card" style="{border}"></div>
        """, unsafe_allow_html=True)

    # Render content if provided
    if content:
        st.write(content)


def status_badge(status, text):
    """Render a status indicator badge.

    Args:
        status: One of 'success', 'warning', 'error', 'pending'
        text: Status text to display

    Returns:
        None (renders to Streamlit)
    """
    status_class = status if status in ['success', 'warning', 'error', 'pending'] else 'pending'

    st.markdown(f"""
    <div class="tech-status-badge">
        <span class="tech-status-dot {status_class}"></span>
        <span>{text}</span>
    </div>
    """, unsafe_allow_html=True)


def page_header(title, subtitle=None):
    """Render a page header.

    Args:
        title: Page title
        subtitle: Optional subtitle

    Returns:
        None (renders to Streamlit)
    """
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color: {COLORS['text_muted']};'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: {SPACING['lg']}'></div>", unsafe_allow_html=True)


def connection_status_card(is_connected, host=None, auth_method=None):
    """Render connection status card in sidebar.

    Args:
        is_connected: Whether connected to Databricks
        host: Optional host URL (if connected)
        auth_method: Optional auth method (if connected)

    Returns:
        None (renders to Streamlit)
    """
    st.markdown(f"""
    <div class="tech-card" style="background: {COLORS['background_secondary']};">
    """, unsafe_allow_html=True)

    if is_connected:
        status_badge('success', '✓ Connected')
        if host:
            st.markdown(f"**Host:** {host}")
        if auth_method:
            st.markdown(f"**Auth:** {auth_method}")
    else:
        status_badge('warning', '⚠ Not Connected')

    st.markdown("</div>", unsafe_allow_html=True)


def action_card(title, description, button_label, button_type="primary", on_click=None, key=None):
    """Render an action card for the welcome page.

    Args:
        title: Card title
        description: One-line description
        button_label: Button text
        button_type: 'primary' or 'secondary'
        on_click: Optional callback function
        key: Optional key for the button

    Returns:
        None (renders to Streamlit)
    """
    st.markdown(f"""
    <div class="tech-card" style="height: 100%;">
        <h3 style="margin-bottom: {SPACING['xs']};">{title}</h3>
        <p style="color: {COLORS['text_muted']}; margin-bottom: {SPACING['md']};">{description}</p>
    </div>
    """, unsafe_allow_html=True)

    # Single button call - on_click handles callback, no if-statements needed
    st.button(
        button_label,
        key=key,
        use_container_width=True,
        type="primary" if button_type == "primary" else None,
        on_click=on_click
    )
