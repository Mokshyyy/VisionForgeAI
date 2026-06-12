import streamlit as st

from core.project_manager import ProjectManager


# Initialize manager
manager = ProjectManager()

# Initialize active project state
if "active_project" not in st.session_state:
    st.session_state.active_project = None


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

if st.session_state.active_project:

    active = st.session_state.active_project

    st.success(
        f"🟢 Active Project: {active['name']} "
        f"(ID: {active['id']})"
    )

    if st.button("Close Current Project"):

        st.session_state.active_project = None
        st.rerun()


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

            col1, col2, col3 = st.columns([5, 1, 1])


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
                    "📂 Open",
                    key=f"open_{project['id']}"
                ):

                    st.session_state.active_project = {
                        "id": project["id"],
                        "name": project["name"]
                    }

                    st.success(
                        f"Opened {project['name']}"
                    )

                    st.rerun()


            
            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{project['id']}"
                ):
                    if (
                        st.session_state.active_project
                        and
                        st.session_state.active_project["id"] == project["id"]
                    ):
                        st.session_state.active_project = None

                    manager.delete_project(
                        project["id"]
                    )

                    st.success(
                        "Project deleted successfully."
                    )

                    st.rerun()