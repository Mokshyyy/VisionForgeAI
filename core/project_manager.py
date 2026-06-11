import uuid
from datetime import datetime
from pathlib import Path

from config import PROJECTS_DIR
from utils.file_utils import save_json, load_json


class ProjectManager:

    def __init__(self):
        self.projects_dir = PROJECTS_DIR


    def create_project(self, name: str, description: str):

        project_id = str(uuid.uuid4())[:8]

        project_data = {
            "id": project_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "dataset_classes": 0,
            "total_images": 0,
            "models": [],
            "status": "Created"
        }

        save_json(
            project_data,
            self.projects_dir / f"{project_id}.json"
        )

        return project_data


    def list_projects(self):

        projects = []

        for file in self.projects_dir.glob("*.json"):
            projects.append(
                load_json(file)
            )

        projects.sort(
            key=lambda x: x["created_at"],
            reverse=True
        )

        return projects


    def delete_project(self, project_id: str):

        project_file = (
            self.projects_dir /
            f"{project_id}.json"
        )

        if project_file.exists():
            project_file.unlink()
            return True

        return False


    def get_project(self, project_id: str):

        project_file = (
            self.projects_dir /
            f"{project_id}.json"
        )

        if project_file.exists():
            return load_json(project_file)

        return None