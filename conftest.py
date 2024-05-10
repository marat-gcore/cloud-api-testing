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


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://cloud-api-preprod.cloud.gc.onl",
        help="Base url for requests"
    )
    parser.addoption(
        "--project",
        action="store",
        default="516070",
        help="ID of the project"
    )
    parser.addoption(
        "--region",
        action="store",
        default="4",
        help="ID of the region"
    )


@pytest.fixture(scope='class')
@allure.title("Prepare an ID of the project")
def project_id(request):
    return request.config.getoption("--project")


@pytest.fixture(scope='class')
@allure.title("Prepare an ID of the region")
def region_id(request):
    return request.config.getoption("--region")


@pytest.fixture(scope='class')
@allure.title("Getting a bearer token...")
def bearer_token():
    username = os.getenv('USERNAME_PREPROD')
    password = os.getenv('PASSWORD')
    auth_url = "https://api.preprod.world/iam/auth/jwt/login"
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
def client_images(bearer_token, project_id, region_id, request):
    base_url = request.config.getoption("--url")

    client = ImagesRequests(
        base_url=f"{base_url}",
        token=bearer_token,
        project_id=project_id,
        region_id=region_id
    )
    client.set_session_authentication()
    yield client
    logger.info(f"\nSession was closed")
    client.session.close()


@pytest.fixture(scope='class')
@allure.title("Prepare a task object")
def client_tasks(bearer_token, request):
    base_url = request.config.getoption("--url")

    client = TasksRequests(base_url=f"{base_url}", token=bearer_token)
    client.set_session_authentication()
    return client


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
            logger.debug("\nThe image was created")
            return response_img
        else:
            logger.debug("\nCreating an image... \n'task_state' is not FINISHED yet")
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

