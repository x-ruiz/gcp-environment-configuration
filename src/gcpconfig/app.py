from utils.project import Project


def main():
    print("Hello World")
    project = Project(name="GCP ENV CONFIG", project_id="gcp-env-configuration")
    project.create_project()
