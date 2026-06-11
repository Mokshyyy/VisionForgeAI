from datetime import datetime
import uuid
import shutil
from typing import Optional

from config import (
    PROJECTS_DIR,
    DATASETS_DIR,
    MODELS_DIR,
    EXPERIMENTS_DIR
)

from utils.file_utils import (
    save_json,
    load_json,
    ensure_directory
)


class ProjectManager:
    """
    Handles complete lifecycle of VisionForge projects.
    
    Responsibilities:
    - Create projects
    - Store metadata
    - Manage project folders
    - Retrieve projects
    - Delete projects safely
    """

    def __init__(self):
        self.projects_dir = PROJECTS_DIR


    def create_project(
        self,
        name: str,
        description: str
    ) -> dict:
        """
        Creates a new AI project.
        """

        project_id = str(uuid.uuid4())[:8]


        # Create storage folders for this project
        for directory in [
            DATASETS_DIR / project_id,
            MODELS_DIR / project_id,
            EXPERIMENTS_DIR / project_id
        ]:
            ensure_directory(directory)


        project_metadata = {
            "id": project_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "status": "Created",

            # Dataset info
            "dataset": {
                "classes": 0,
                "images": 0
            },

            # Model information
            "models": [],
            "active_model": None
        }


        metadata_path = (
            self.projects_dir /
            f"{project_id}.json"
        )


        save_json(
            project_metadata,
            metadata_path
        )


        return project_metadata


    def list_projects(self) -> list:
        """
        Returns all projects sorted by creation date.
        """

        projects = []


        for file in self.projects_dir.glob("*.json"):
            try:
                projects.append(
                    load_json(file)
                )

            except Exception as error:
                print(
                    f"Failed loading {file}: {error}"
                )


        projects.sort(
            key=lambda project: project["created_at"],
            reverse=True
        )

        return projects


    def get_project(
        self,
        project_id: str
    ) -> Optional[dict]:
        """
        Returns a single project.
        """

        project_file = (
            self.projects_dir /
            f"{project_id}.json"
        )


        if project_file.exists():
            return load_json(project_file)

        return None


    def delete_project(
        self,
        project_id: str
    ) -> bool:
        """
        Completely removes a project and all associated data.
        """

        project_file = (
            self.projects_dir /
            f"{project_id}.json"
        )


        if project_file.exists():
            project_file.unlink()


        # Remove all associated folders
        for directory in [
            DATASETS_DIR / project_id,
            MODELS_DIR / project_id,
            EXPERIMENTS_DIR / project_id
        ]:

            if directory.exists():
                shutil.rmtree(directory)


        return True


    def update_project(
        self,
        project_id: str,
        data: dict
    ) -> bool:
        """
        Updates project metadata.
        """

        project_file = (
            self.projects_dir /
            f"{project_id}.json"
        )


        if not project_file.exists():
            return False


        save_json(
            data,
            project_file
        )


        return True