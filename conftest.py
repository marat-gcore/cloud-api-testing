import os
import logging
import time
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
        logger.error(f"\nRequest error when receiving a token: {e}")
        raise
    except ValueError as e:
        logger.error(f"\nError when processing a token: {e}")
        raise


@pytest.fixture(scope='class')
@allure.title("Prepare HTTP client for requests")
def client_images(bearer_token):
    base_url = os.getenv('PREPROD_URL')

    img_req = ImagesRequests(base_url=f"{base_url}", token=bearer_token)
    img_req.set_session_authentication()
    yield img_req
    logger.info(f"\nSession was closed")
    img_req.session.close()


@pytest.fixture(scope='class')
@allure.title("Prepare a task object")
def client_tasks(bearer_token):
    base_url = os.getenv('PREPROD_URL')

    task_req = TasksRequests(base_url=f"{base_url}", token=bearer_token)
    task_req.set_session_authentication()
    return task_req


@pytest.fixture(scope='class')
@allure.title("Prepare request body")
def img_request_body():
    return {
        'name': 'qa-img-fixture',
        'volume_id': '4d188668-8a16-44f9-9896-a50d4110cd8e'
    }


@pytest.fixture(scope='class')
@allure.title("Create image")
def create_img(client_images, client_tasks, img_request_body):
    response_img = client_images.create_image(img_request_body)
    response_body = response_img.json()
    task_id = ''.join(response_body.get("tasks"))

    timeout = 120
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = client_tasks.get_task_by_id(task_id)
        task_state = response.json()["state"]
        if task_state == "FINISHED":
            logger.debug("\nThe image was created, 'task_state' is FINISHED")
            return response_img
        else:
            logger.debug("\nCreating an image... 'task_state' is not FINISHED yet")
            time.sleep(5)
    logger.error("\nImage creation failed by time out")


@pytest.fixture(scope='class')
@allure.title("Prepare image ID / Clean image")
def image_id(client_images, create_img, img_request_body):
    request_key = "name"
    request_value = img_request_body.get(request_key)

    response = client_images.get_images()
    img_id = BaseAssertion.assert_obj_found(response, request_key, request_value)
    return img_id

