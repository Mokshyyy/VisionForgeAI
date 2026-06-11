import streamlit as st

from core.project_manager import ProjectManager


manager = ProjectManager()


st.title("📁 Project Workspace")

st.markdown(
    "Create and manage your AI projects."
)


with st.expander("➕ Create New Project"):

    name = st.text_input(
        "Project Name"
    )

    description = st.text_area(
        "Project Description"
    )

    if st.button("Create Project"):

        if name.strip():

            manager.create_project(
                name,
                description
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


projects = manager.list_projects()


if not projects:

    st.info(
        "No projects created yet."
    )

else:

    st.subheader(
        "Your Projects"
    )

    for project in projects:

        with st.container(border=True):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.markdown(
                    f"""
### {project['name']}

**ID:** {project['id']}

{project['description']}

Created: {project['created_at']}

Dataset Classes: {project['dataset_classes']}

Images: {project['total_images']}

Status: {project['status']}
"""
                )

            with col2:

                if st.button(
                    "🗑️ Delete",
                    key=project["id"]
                ):

                    manager.delete_project(
                        project["id"]
                    )

                    st.success(
                        "Deleted!"
                    )

                    st.rerun()