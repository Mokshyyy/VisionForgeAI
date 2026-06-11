import streamlit as st

from core.project_manager import ProjectManager


# Initialize manager
manager = ProjectManager()


# -----------------------------
# Page Header
# -----------------------------

st.title("📁 Project Workspace")

st.markdown(
    """
    Create and manage your AI projects.
    Every project contains its own datasets,
    experiments, and trained models.
    """
)


# -----------------------------
# Create New Project
# -----------------------------

with st.expander(
    "➕ Create New Project",
    expanded=False
):

    project_name = st.text_input(
        "Project Name"
    )

    project_description = st.text_area(
        "Project Description"
    )


    if st.button(
        "Create Project",
        type="primary"
    ):

        if project_name.strip():

            manager.create_project(
                project_name,
                project_description
            )

            st.success(
                "Project created successfully!"
            )

            st.rerun()

        else:

            st.error(
                "Project name cannot be empty."
            )


st.divider()


# -----------------------------
# Display Existing Projects
# -----------------------------

projects = manager.list_projects()


if not projects:

    st.info(
        "No projects available. Create your first AI project!"
    )


else:

    st.subheader(
        "Your Projects"
    )


    for project in projects:

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [5, 1]
            )


            # Project Details
            with col1:

                st.markdown(
                    f"""
### {project['name']}

**Project ID:** `{project['id']}`

**Description:**  
{project['description']}

**Created:** {project['created_at']}

**Dataset**
- Classes: {project['dataset']['classes']}
- Images: {project['dataset']['images']}

**Models:** {len(project['models'])}
                    """
                )


            # Actions
            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{project['id']}"
                ):

                    manager.delete_project(
                        project["id"]
                    )

                    st.success(
                        "Project deleted successfully."
                    )

                    st.rerun()