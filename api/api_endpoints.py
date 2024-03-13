from enum import Enum
import os
from dotenv import load_dotenv


load_dotenv()


class ImagesEndpoints(str, Enum):
    IMAGES = f"/v1/images/{os.getenv('PROJECT_ID')}/{os.getenv('REGION_ID')}"

    def __str__(self) -> str:
        return self.value
