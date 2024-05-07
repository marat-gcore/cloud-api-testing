import os
import logging

from api.api_session import Session
from api.api_data import TokenType

logger = logging.getLogger("logger_api_client")


class APIClient:
    TASKS = "/v1/tasks"
    IMAGES = f"/v1/images/{os.getenv('PROJECT_ID')}/{os.getenv('REGION_ID')}"

    def __init__(self, base_url: str, token: str):
        logger.info(f"\nSession initialized")
        self.base_url = base_url
        self.token = token
        self.session = Session()

    def get_header(self, key: str) -> str:
        if not self.session.headers.get(key):
            logger.error(f"\nThe expected key '{key}' is missing in headers.")
            raise ValueError(f"The expected key '{key}' is missing in headers.")
        header_value: str | bytes = self.session.headers[key]
        if isinstance(header_value, bytes):
            return header_value.decode("utf-8")
        return header_value

    def add_header(self, key: str, value: str):
        """
        To hide refresh token from logs
        """
        logs_value = value
        if key == "refresh":
            logs_value = "****"
        logger.debug(f'\nSetting header "{key}" as "{logs_value}"')
        self.session.headers.update({key: value})

    def set_session_authentication(self):
        self.token = f"{TokenType.BEARER} {self.token}"
        self.session.headers.update({"Authorization": f"{self.token}"})

    def set_session_authentication_with_permanent_token(self) -> None:
        if TokenType.APIKEY not in self.token:
            self.token = f"{TokenType.APIKEY} {self.token}"
        self.session.headers.update({"Authorization": f"{self.token}"})

    def get_obj(self, endpoint, headers, params=None):
        return self.session.get(url=f"{self.base_url}{endpoint}", headers=headers, params=params)

    def post_obj(self, endpoint, headers, **kwargs):
        return self.session.post(url=f"{self.base_url}{endpoint}", headers=headers, **kwargs)

    def patch_obj(self, endpoint, headers, **kwargs):
        return self.session.patch(url=f"{self.base_url}{endpoint}", headers=headers, **kwargs)

    def delete_obj(self, endpoint, headers):
        return self.session.delete(url=f"{self.base_url}{endpoint}", headers=headers)

    def __str__(self) -> str:
        token_data = f"{self.token[0:10]}...{self.token[-5:]}" if self.token else "'token_data' is null"
        return f"<BASE URL: {self.base_url};" f" TOKEN: {token_data};" f" HEADERS: {self.session.headers}>"
