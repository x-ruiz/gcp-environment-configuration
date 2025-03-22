import json
import requests
import os
import subprocess
import yaml

from .logger import get_logger
from .api import Api

logger = get_logger(__name__)


class Project:
    url = "https://cloudresourcemanager.googleapis.com/v3/projects/"
    # TODO: Need to add a billing account property (instance not class)

    def __init__(self, project_id: str, name: str = ""):
        self.name = name
        self.project_id = project_id

    def create_project(self) -> bool:
        logger.info(f"Creating project with name {self.name} and id {self.project_id}")
        data = {"projectId": self.project_id, "displayName": self.name}
        api = Api()
        response = api.request(url=self.url, data=data)

        if response == 200:
            logger.info(f"Created project successfully {self.project_id}")
            return True
        elif response == 409:
            logger.info(f"Project {self.project_id} already exists, continuing...")
            return True
        else:
            logger.error(f"Unsuccessful project creation for {self.project_id}")
            return False

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

    # TODO: need to create a method that attaches a project to a billing account
    # We can assume billing account is created outside this CLI since it has to be done
    # through UI

    def set_billing(self, billing_id: str):
        # gcloud billings projects link <project_id> --billing-account=<billing_id>
        self.billing_id = billing_id

    def assign_billing(self) -> bool:
        logger.info(f"Assigning billing account {self.billing_id} for project {self.project_id}")
        command = f"gcloud billing projects link {self.project_id} --billing-account={self.billing_id}"
        subprocess.run(command, shell=True, capture_output=True, check=True)
        is_billing = self.check_billing()

    def check_billing(self) -> bool:
        output = subprocess.run(f"gcloud billing projects describe {self.project_id}", shell=True, capture_output=True, check=True)
        yml = yaml.safe_load(output.stdout.decode("utf-8"))
        billing_account = yml["billingAccountName"]

        if billing_account == '':
            logger.warn(f"Billing account not linked to project {self.project_id}")
            return False
        else:
            logger.info(f"Billing account {billing_account} set for project {self.project_id}")
            return True

    def set_apis(self, apis: str):
        logger.info(f"Setting apis for project: {self.project_id} -> apis: {apis} - this might take a while...")
        apis = apis.replace(",", " ")
        command = f"gcloud services enable {apis}"
        output = subprocess.run(command, shell=True, capture_output=True, check=True)
        if output.stdout:
            logger.debug("\n" + output.stdout.decode("utf-8"))

        if output.stderr:
            logger.debug("\n" + output.stderr.decode("utf-8"))

        # Print out enabled apis
        output = subprocess.run(f"gcloud services list --enabled --project {self.project_id}", shell=True, capture_output=True, check=True)
        logger.info("\n" + output.stdout.decode("utf-8"))
