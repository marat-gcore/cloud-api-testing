import os
import pytest
import time
from api.api_client import ApiClient
from api.api_requests import ImagesRequests
from assertions.assertion_base import BaseAssertion
from utilities.json_utils import convert_json


@pytest.fixture(scope='class')
def client():
    return ApiClient()


@pytest.fixture(scope='class')
def bearer_token(client):
    data = {"username": f"{os.getenv('USERNAME_PREPROD')}", "password": f"{os.getenv('PASSWORD')}"}
    response = client.post(f"https://{os.getenv('API_AUTH')}", json=data)
    return response.json().get("access")


@pytest.fixture(scope='class')
def image_obj(client, bearer_token):
    return ImagesRequests(client, bearer_token)


@pytest.fixture(scope='class')
def img_request_body():
    request_body = {
        'name': 'qa-img-fixture',
        'volume_id': '43aff485-5154-499d-a8f1-e9efba93fc30'
    }    
    return request_body


@pytest.fixture(scope='class')
def create_img(image_obj, img_request_body):    
    response = image_obj.create_image(img_request_body)
    time.sleep(100)
    return response


@pytest.fixture(scope='class')
def image_id(image_obj, create_img, img_request_body):
    request_key = "name"
    request_value = img_request_body.get(request_key)

    response = image_obj.get_images()
    response_body = convert_json(response)
    img_id = BaseAssertion.assert_obj_found(response_body, request_key, request_value)
    yield img_id
    image_obj.delete_image(img_id)
