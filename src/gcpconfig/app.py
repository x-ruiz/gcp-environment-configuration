import fire
import subprocess

from utils.project import Project
from utils.logger import get_logger


logger = get_logger(__name__)


class App:
    def create_project(self, name: str, project_id: str) -> Project:
        project = Project(name=name, project_id=project_id)
        project.create_project()
        return project

    def set_api(self, project_id: str, apis: str):
        """Sets one or multiple google apis for a given project id.

        Args:
            projectid: The google project id to set apis for
            apis: Comma separated string to set apis (pubsub.googleapis.com,containerregistry.googleapis.com)
        """

        project = Project(project_id=project_id)
        project.set_project()
        project.set_apis(apis=apis)

    def create_and_set_project(self, name: str, project_id: str):
        project = Project(name=name, project_id=project_id)
        project.create_project()
        logger.info(f"Creating and setting gcloud config project to {project.name}")
        project.set_project()

    def create_and_set_apis(self, name: str, project_id: str, apis: str):
        project = Project(name=name, project_id=project_id)
        success = project.create_project()
        project.set_project()
        if success == True:
            project.set_apis(apis)
        else:
            logger.error("Project creation failed, skipping api setting...")



def main():
    app = App()
    fire.Fire(app)
