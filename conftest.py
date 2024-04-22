import os
import time
import pytest
import allure
import requests
from api.api_requests import ImagesRequests, TasksRequests
from assertions.assertion_base import BaseAssertion
# from dotenv import load_dotenv


# load_dotenv()


@pytest.fixture(scope='class')
@allure.title("Prepare HTTP client")
def client():
    yield requests.Session()
    requests.Session().close()


@pytest.fixture(scope='class')
@allure.title("Prepare a bearer token")
def bearer_token(client):
    data = {"username": f"{os.getenv('USERNAME_PREPROD')}", "password": f"{os.getenv('PASSWORD')}"}
    response = client.post(f"https://api.preprod.world/iam/auth/jwt/login", json=data)
    # response = client.post(f"https://{os.getenv('API_AUTH')}", json=data)
    return response.json().get("access")


@pytest.fixture(scope='class')
@allure.title("Prepare an image object")
def image_obj(client, bearer_token):
    return ImagesRequests(client, bearer_token)


@pytest.fixture(scope='class')
@allure.title("Prepare a task object")
def task_obj(client, bearer_token):
    return TasksRequests(client, bearer_token)


@pytest.fixture(scope='class')
@allure.title("Prepare request body")
def img_request_body():
    return {
        'name': 'qa-img-fixture',
        'volume_id': 'fbfb26d1-37d9-4bd9-82f6-e1d0fd3091c8'
    }


@pytest.fixture(scope='class')
@allure.title("Create image")
def create_img(image_obj, task_obj, img_request_body):
    response_img = image_obj.create_image(img_request_body)
    response_body_img = response_img.json()
    task_id = ''.join(response_body_img.get("tasks"))

    timeout = 120
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = task_obj.get_task_by_id(task_id)
        task_state = response.json()["state"]
        if task_state == "FINISHED":
            return response_img
        else:
            time.sleep(5)
    print("Image creation failed by time out")


@pytest.fixture(scope='class')
@allure.title("Prepare image ID / Clean image")
def image_id(image_obj, create_img, img_request_body):
    request_key = "name"
    request_value = img_request_body.get(request_key)
    response = image_obj.get_images()
    
    img_id = BaseAssertion.assert_obj_found(response, request_key, request_value)
    yield img_id
    image_obj.delete_image(img_id)
