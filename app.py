import streamlit as st

from utils.file_utils import initialize_storage


# Create storage folders
initialize_storage()


st.set_page_config(
    page_title="VisionForge AI",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 VisionForge AI")

st.markdown("""
## Build Custom Computer Vision Models Without Code

Welcome to VisionForge.

This platform allows you to:

- 📁 Create AI projects
- 🖼️ Manage image datasets
- 🧪 Train custom models
- 📊 Compare experiments
- 🧠 Manage model versions
- 🔮 Run predictions
""")


st.info(
    "Use the sidebar to navigate through the AI development pipeline."
)