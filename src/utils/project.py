import json
import requests
import os
import subprocess

from .logger import get_logger

logger = get_logger(__name__)


class Project:
    url = "https://cloudresourcemanager.googleapis.com/v1/projects/"
    access_token = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    def __init__(self, name: str, project_id: str):
        self.name = name
        self.project_id = project_id

    def create_project(self):
        logger.info(f"Creating project with name {self.name} and id {self.project_id}")
        data = {"projectId": self.project_id, "name": self.name}
        try:
            response = requests.post(
                self.url,
                json=data,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            logger.info(f"Project created | {self.name} | {self.project_id}")
            logger.debug(f"Response Status Code: {response.status_code}")
            logger.debug(f"Response Body: {response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error {e}")
        except json.JSONDecodeError:
            logger.error("Response is not valid JSON")
