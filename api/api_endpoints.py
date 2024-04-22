import os
from enum import Enum


class Endpoints(str, Enum):
    TASKS = f"https://{os.getenv('PREPROD_URL')}/v1/tasks"
    IMAGES = f"https://cloud-api-preprod.cloud.gc.onl/v1/images/{os.getenv('PROJECT_ID')}/{os.getenv('REGION_ID')}"
    # IMAGES = f"https://{os.getenv('PREPROD_URL')}/v1/images/{os.getenv('PROJECT_ID')}/{os.getenv('REGION_ID')}"

    def __str__(self) -> str:
        return self.value
