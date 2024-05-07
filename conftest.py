import os
import logging
import pytest
import allure
import requests

from api.api_requests import ImagesRequests, TasksRequests
from assertions.assertion_base import BaseAssertion

logger = logging.getLogger("logger_fixtures")


def pytest_configure():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope='class')
@allure.title("Prepare a bearer token")
def bearer_token():
    username = os.getenv('USERNAME_PREPROD')
    password = os.getenv('PASSWORD')
    auth_url = os.getenv('API_AUTH')
    data = {
        "username": f"{username}",
        "password": f"{password}"
    }

    if not username or not password or not auth_url:
        raise ValueError(f"Required 'username' or 'password' or 'auth_url' is missing")

    try:
        response = requests.post(url=f"{auth_url}", json=data)
        token = response.json().get("access")
        if not token:
            raise ValueError("Fail to get bearer token")
        return token
    except requests.RequestException as e:
        logger.error(f"Request error when receiving a token: {e}")
        raise
    except ValueError as e:
        logger.error(f"Error when processing a token: {e}")
        raise


@pytest.fixture(scope='class')
@allure.title("Prepare HTTP client for requests")
def client_images(bearer_token):
    base_url = os.getenv('PREPROD_URL')

    img_req = ImagesRequests(base_url=f"{base_url}", token=bearer_token)
    yield img_req
    logger.info(f"The session was closed")
    img_req.session.close()


# @pytest.fixture(scope='class')
# @allure.title("Prepare a task object")
# def task_obj(client, bearer_token):
#     return TasksRequests(client, bearer_token)


# @pytest.fixture(scope='class')
# @allure.title("Prepare request body")
# def img_request_body():
#     return {
#         'name': 'qa-img-fixture',
#         'volume_id': 'fbfb26d1-37d9-4bd9-82f6-e1d0fd3091c8'
#     }


# @pytest.fixture(scope='class')
# @allure.title("Create image")
# def create_img(image_obj, task_obj, img_request_body):
#     response_img = image_obj.create_image(img_request_body)
#     response_body_img = response_img.json()
#     task_id = ''.join(response_body_img.get("tasks"))
#
#     timeout = 120
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         response = task_obj.get_task_by_id(task_id)
#         task_state = response.json()["state"]
#         if task_state == "FINISHED":
#             return response_img
#         else:
#             time.sleep(5)
#     print("Image creation failed by time out")


# @pytest.fixture(scope='class')
# @allure.title("Prepare image ID / Clean image")
# def image_id(image_obj, create_img, img_request_body):
#     request_key = "name"
#     request_value = img_request_body.get(request_key)
#     response = image_obj.get_images()
#
#     img_id = BaseAssertion.assert_obj_found(response, request_key, request_value)
#     yield img_id
#     image_obj.delete_image(img_id)
