import fire

from utils.project import Project
from utils.logger import get_logger


logger = get_logger(__name__)

class App():
    def create_project(self, name: str, project_id: str):
        project = Project(name=name, project_id=project_id)
        project.create_project()

def main():
    app = App()
    fire.Fire(app)
