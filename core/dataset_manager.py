from pathlib import Path
from PIL import Image
import shutil

from config import DATASETS_DIR
from core.project_manager import ProjectManager


class DatasetManager:
    """
    Handles dataset operations:
    - Class management
    - Image validation
    - Upload handling
    - Dataset statistics
    """

    def __init__(self):
        self.datasets_dir = DATASETS_DIR
        self.project_manager = ProjectManager()


    def create_class(self, project_id: str, class_name: str) -> bool:
        """
        Creates a new dataset class folder.
        """

        class_path = (
            self.datasets_dir /
            project_id /
            class_name
        )

        if class_path.exists():
            return False

        class_path.mkdir(parents=True)

        self.update_dataset_stats(project_id)

        return True
    

    def delete_class(
        self,
        project_id: str,
        class_name: str
    ) -> bool:
        """
        Deletes a dataset class and all its images.
        """

        class_path = (
            self.datasets_dir /
            project_id /
            class_name
        )

        if not class_path.exists():
            return False


        shutil.rmtree(
            class_path
        )


        self.update_dataset_stats(
            project_id
        )

        return True


    def upload_images(
        self,
        project_id: str,
        class_name: str,
        uploaded_files: list
    ) -> tuple:
        """
        Uploads images to a dataset class.
        
        Returns:
            (successful_uploads, failed_uploads)
        """

        class_path = (
            self.datasets_dir /
            project_id /
            class_name
        )

        success_count = 0
        failed_files = []


        for file in uploaded_files:

            file_path = class_path / file.name


            # Prevent duplicate filenames
            if file_path.exists():
                failed_files.append(
                    f"{file.name} (duplicate)"
                )
                continue


            # Validate image
            if not self.validate_image(file):
                failed_files.append(
                    f"{file.name} (invalid image)"
                )
                continue


            # Save image
            file.seek(0)

            with open(file_path, "wb") as destination:
                shutil.copyfileobj(
                    file,
                    destination
                )

            success_count += 1


        self.update_dataset_stats(project_id)

        return success_count, failed_files
    
    def validate_image(self, file) -> bool:
        """
        Checks if uploaded file is a valid image.
        """

        try:
            img = Image.open(file)
            img.verify()
            return True

        except Exception:
            return False
        
        
    def get_classes(
        self,
        project_id: str
    ) -> list:
        """
        Returns all classes in a project dataset.
        """

        project_path = (
            self.datasets_dir /
            project_id
        )

        if not project_path.exists():
            return []


        classes = [
            folder.name
            for folder in project_path.iterdir()
            if folder.is_dir()
        ]


        return sorted(classes)
    
    def get_dataset_statistics(
        self,
        project_id: str
    ) -> dict:
        """
        Calculates dataset statistics from folders.
        """

        project_dataset_path = (
            self.datasets_dir /
            project_id
        )

        classes = 0
        images = 0


        for class_folder in project_dataset_path.iterdir():

            if class_folder.is_dir():

                classes += 1

                images += len(
                    [
                        file
                        for file in class_folder.iterdir()
                        if file.is_file()
                    ]
                )


        return {
            "classes": classes,
            "images": images
        }
    
    def update_dataset_stats(
        self,
        project_id: str
    ):
        """
        Updates project metadata with latest dataset statistics.
        """

        project = self.project_manager.get_project(
            project_id
        )


        if not project:
            return


        stats = self.get_dataset_statistics(
            project_id
        )


        project["dataset"] = stats


        self.project_manager.update_project(
            project_id,
            project
        )