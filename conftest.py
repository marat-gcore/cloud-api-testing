import os
import pytest
import allure
import time
from httpx import Client
from api.api_requests import ImagesRequests
from assertions.assertion_base import BaseAssertion


@pytest.fixture(scope='class')
@allure.title("Prepare HTTP client")
def client():
    return Client()


@pytest.fixture(scope='class')
@allure.title("Prepare a bearer token")
def bearer_token(client):
    data = {"username": f"{os.getenv('USERNAME_PREPROD')}", "password": f"{os.getenv('PASSWORD')}"}
    response = client.post(f"https://{os.getenv('API_AUTH')}", json=data)
    return response.json().get("access")


@pytest.fixture(scope='class')
@allure.title("Prepare an image object")
def image_obj(client, bearer_token):
    return ImagesRequests(client, bearer_token)


@pytest.fixture(scope='class')
@allure.title("Prepare request body")
def img_request_body():
    return {
        'name': 'qa-img-fixture',
        'volume_id': '43aff485-5154-499d-a8f1-e9efba93fc30'
    }


@pytest.fixture(scope='class')
@allure.title("Create image")
def create_img(image_obj, img_request_body):    
    response = image_obj.create_image(img_request_body)
    time.sleep(100)
    return response


@pytest.fixture(scope='class')
@allure.title("Prepare image ID / Clean image")
def image_id(image_obj, create_img, img_request_body):
    request_key = "name"
    request_value = img_request_body.get(request_key)
    response = image_obj.get_images()
    
    img_id = BaseAssertion.assert_obj_found(response, request_key, request_value)
    yield img_id
    image_obj.delete_image(img_id)
