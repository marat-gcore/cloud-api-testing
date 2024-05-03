import json
import logging
import uuid
import requests

from datetime import datetime, timezone
from typing import Dict, Tuple, Any

logger = logging.getLogger("api_tests")


class Session(requests.Session):
    """
    requests.Session with verbose logging
    """

    # def __init__(self, user_agent_header: Dict):
    #     super().__init__()
    #     self.user_agent_header = user_agent_header

    @staticmethod
    def get_current_data() -> str:
        now: datetime = datetime.now(timezone.utc)
        date_format = "%a, %d %b %Y %H:%M:%S GMT"
        return now.strftime(date_format)

    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs: Any):
        json_data = kwargs.pop("json", None)
        raw_data = kwargs.pop("data", None)
        log_level = kwargs.pop("log_level", logging.INFO)

        if isinstance(method, bytes):
            method = method.decode("utf-8")
        if isinstance(url, bytes):
            url = url.decode("utf-8")
        logger.info(f"Request: {method.upper()} to {url} with {kwargs}")

        headers = {}
        # headers.update(self.user_agent_header)
        headers.update({"X-Request-ID": str(uuid.uuid4())})
        headers.update({"Date": self.get_current_data()})
        headers.update(kwargs.pop("headers", dict()))
        logger.info(f"Request headers: {headers}")

        if json_data:
            logger.log(log_level, f"Request body:\n{json.dumps(json_data, indent=2, sort_keys=True)}")
        if raw_data:
            logger.log(log_level, f"Request body:\n{raw_data}")

        response = super().request(
            method,
            url,
            json=json_data,
            data=raw_data,
            headers=headers,
            **kwargs,
        )
        return response
