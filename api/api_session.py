import json
import logging
import uuid
import requests

from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("logger_session")


class Session(requests.Session):
    """
    requests.Session with verbose logging
    """

    @staticmethod
    def get_current_data() -> str:
        now: datetime = datetime.now(timezone.utc)
        date_format = "%a, %d %b %Y %H:%M:%S GMT"
        return now.strftime(date_format)

    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs: Any):
        json_data = kwargs.pop("json", None)
        raw_data = kwargs.pop("data", None)

        if isinstance(method, bytes):
            method = method.decode("utf-8")
        if isinstance(url, bytes):
            url = url.decode("utf-8")

        headers = kwargs.pop("headers", {})
        headers.update({"X-Request-ID": str(uuid.uuid4()), "Date": self.get_current_data()})
        headers.update(self.headers)

        if 'Authorization' not in headers:
            logger.error(f"\nAuthorization header is missing in the request to {url}")
            raise ValueError("Authorization header is missing")

        logger.debug(f"\nRequest: {method.upper()} to {url} with {kwargs}")
        # logger.debug(f"Request headers: {headers}")

        if json_data:
            logger.info(f"\nRequest body:\n{json.dumps(json_data, indent=2, sort_keys=True)}")
        if raw_data:
            logger.info(f"\nRequest body:\n{raw_data}")

        response = super().request(
            method,
            url,
            json=json_data,
            data=raw_data,
            headers=headers,
            **kwargs
        )
        return response
