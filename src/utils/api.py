import subprocess
import requests
import json

from utils.logger import get_logger

logger = get_logger(__name__)


class Api:
    access_token = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    def request(self, url: str, data: dict):
        try:
            response = requests.post(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            logger.debug(f"Response Status Code: {response.status_code}")
            logger.debug(f"Response Body: {response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error {e}")
        except json.JSONDecodeError:
            logger.error("Response is not valid JSON")
