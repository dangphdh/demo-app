"""Welcome page - Landing page with templates and tutorial access."""

import streamlit as st

st.set_page_config(
    page_title="Welcome - Metric View Builder",
    page_icon="👋",
    layout="wide"
)

st.title("👋 Welcome to Metric View Builder")
st.markdown("""
This is the welcome page. In Phase 3, this will feature:
- Template gallery
- Interactive tutorial
- Getting started guide
""")

if st.button("Go to Wizard", use_container_width=True, type="primary"):
    st.switch_page("1_wizard.py")
