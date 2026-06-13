import streamlit as st
import time
from core.dataset_manager import DatasetManager


# Initialize manager
manager = DatasetManager()


# Initialize session state
if "active_project" not in st.session_state:
    st.session_state.active_project = None


st.title("📸 Dataset Manager")


# Check if a project is selected
if not st.session_state.active_project:

    st.warning(
        "Please open a project from Project Workspace first."
    )

    st.stop()


# Get current project
project = st.session_state.active_project


st.success(
    f"Working on: {project['name']} "
    f"(ID: {project['id']})"
)

st.divider()

st.subheader("➕ Create Dataset Class")


class_name = st.text_input(
    "Class Name"
)


if st.button(
    "Create Class",
    type="primary"
):

    if class_name.strip():

        success = manager.create_class(
            project["id"],
            class_name.strip()
        )


        if success:

            st.success(
                f"Class '{class_name}' created."
            )
            
            time.sleep(1.5)
            st.rerun()


        else:

            st.error(
                "Class already exists."
            )


    else:

        st.error(
            "Class name cannot be empty."
        )


# =============================
# Dataset Statistics
# =============================

st.divider()

st.subheader("📊 Dataset Statistics")


stats = manager.get_dataset_statistics(
    project["id"]
)


col1, col2 = st.columns(2)


with col1:
    st.metric(
        "Classes",
        stats["classes"]
    )


with col2:
    st.metric(
        "Total Images",
        stats["images"]
    )

# =============================
# Dataset Classes
# =============================

st.divider()

st.subheader("📂 Dataset Classes")


classes = manager.get_classes(
    project["id"]
)


if not classes:

    st.info(
        "No classes created yet."
    )


else:

    for class_name in classes:

        col1, col2 = st.columns([5, 1])


        with col1:

            st.write(
                f"**{class_name}**"
            )


        with col2:

            if st.button(
                "🗑️",
                key=f"delete_class_{class_name}"
            ):

                manager.delete_class(
                    project["id"],
                    class_name
                )

                st.success(
                    f"Deleted class '{class_name}'."
                )

                time.sleep(1.5)
                st.rerun()


# =============================
# Upload Images
# =============================

st.divider()

st.subheader("📤 Upload Images")


classes = manager.get_classes(
    project["id"]
)


if not classes:

    st.info(
        "Create a class before uploading images."
    )


else:

    selected_class = st.selectbox(
        "Select Class",
        classes
    )


    uploaded_files = st.file_uploader(
        "Choose images",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        accept_multiple_files=True
    )


    if st.button(
        "Upload Images",
        type="primary"
    ):

        if uploaded_files:

            success, failed = (
                manager.upload_images(
                    project["id"],
                    selected_class,
                    uploaded_files
                )
            )


            st.success(
                f"{success} images uploaded successfully."
            )


            if failed:

                st.warning(
                    "Some files were skipped:"
                )

                for file in failed:

                    st.write(
                        f"• {file}"
                    )

            time.sleep(1.5)

            st.rerun()


        else:

            st.error(
                "Please select at least one image."
            )