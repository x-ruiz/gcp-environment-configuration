import json
import requests
import os
import subprocess

from .logger import get_logger
from .api import Api

logger = get_logger(__name__)


class Project:
    url = "https://cloudresourcemanager.googleapis.com/v1/projects/"

    def __init__(self, project_id: str, name: str = ""):
        self.name = name
        self.project_id = project_id

    def create_project(self):
        logger.info(f"Creating project with name {self.name} and id {self.project_id}")
        data = {"projectId": self.project_id, "name": self.name}
        api = Api()
        api.request(url=self.url, data=data)

    def set_project(self):
        logger.info(f"Setting current config project to {self.project_id}")
        subprocess.run(
            f"gcloud config set project {self.project_id}",
            shell=True,
            capture_output=True,
            check=True,
        )

        output = subprocess.run(
            f"gcloud config list", shell=True, capture_output=True, check=True
        )
        logger.info("\n" + output.stdout.decode("utf-8"))

    def set_apis(self, apis: str):
        logger.info(f"Setting apis for project: {self.project_id} -> apis: {apis}")
        apis = apis.replace(",", " ")
        command = f"gcloud services enable {apis}"
        subprocess.run(command, shell=True, capture_output=True, check=True)
        # Print out enabled apis
        output = subprocess.run(f"gcloud services list --enabled --project {self.project_id}", shell=True, capture_output=True, check=True)
        logger.info("\n" + output.stdout.decode("utf-8"))
