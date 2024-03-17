import pytest
import json
import time
from http import HTTPStatus
from assertions.assertion_base import BaseAssertion
from models.images import images_models as models


class TestImages:
    """
    /v1/images/<project_id>/<region_id>
    """

    # -------positive-------

    def test_get_list_images(self, image_obj):
        response = image_obj.get_images()

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.ListImages)
        if response.json()["count"] > 0:
            BaseAssertion.assert_schema(response.json()["results"], models.Image)

    def test_get_empty_list_images(self, image_obj):
        response = image_obj.get_images()

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        if response.json()["count"] == 0:
            assert response.json()["results"] == []

    @pytest.mark.parametrize("params", ['private', 'public', 'shared'])
    def test_get_list_images_by_visibility_param(self, image_obj, params):
        query_param = {'visibility': f'{params}'}
        response = image_obj.get_images(query_param)

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        if response.json()['count'] > 0:
            for item in response.json()['results']:
                assert item['visibility'] == f'{params}'

    def test_get_list_images_by_metadata_k_param(self, image_obj):
        tag = 'mar_tag'
        query_param = {'metadata_k': f'{tag}'}
        response = image_obj.get_images(query_param)

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        if response.json()["count"] > 0:
            for item in response.json()['results']:
                for key in item['metadata'].keys():
                    assert key == tag

    def test_get_image_by_id(self, image_obj, image_id):
        response = image_obj.get_image_by_id(image_id)

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.Image)

    def test_get_image_by_id_include_prices_param(self, image_obj, image_id):
        query_param = {'include_prices': True}
        response = image_obj.get_image_by_id(image_id, query_param)

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.ImageWithPrice)

    def test_post_create_image(self, image_obj, img_request_body, create_img):
        request_key = "name"
        request_value = img_request_body.get(request_key)

        BaseAssertion.assert_status_code(create_img, HTTPStatus.OK)
        BaseAssertion.assert_schema(create_img, models.RequestSuccessful)

        response = image_obj.get_images()
        BaseAssertion.assert_obj_found(response, request_key, request_value)

    def test_patch_update_image(self, image_obj, img_request_body, image_id):
        request_body = {
            'name': 'qa-img-changed'
        }
        request_key = 'name'
        request_value = request_body[request_key]

        response = image_obj.update_image(image_id, request_body)
        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.Image)
        time.sleep(2)

        response = image_obj.get_image_by_id(image_id)
        response_body = response.json()
        assert request_value == response_body.get(request_key)

    def test_delete_image(self, image_obj, image_id):
        response = image_obj.delete_image(image_id)
        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.RequestSuccessful)
        time.sleep(2)

        response = image_obj.get_image_by_id(image_id)
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    # -------negative-------

    def test_get_list_images_bad_request(self, image_obj):
        query_param = {'visibility': 'somevalue'}
        response = image_obj.get_images(query_param)

        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.BadRequest)

    def test_get_image_not_exist_id(self, image_obj):
        image_id = "23003df3-e509-4bc9-ad4b-5f77ad40da691"
        response = image_obj.get_image_by_id(image_id)

        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    @pytest.mark.xfail
    @pytest.mark.parametrize("img_id", [
            "23003df3-e509-4bc9-ad4b-5f77ad40da69435",
            "34523003df3-e509-4bc9-ad4b-5f77ad40da69",
            "23003df3-e509-4b45c9-ad4b-5f77ad40da69",
            "23003df3-e509-4bc9-ad4b-5f77ad40da69!@#?$",
            "!@#.$%23003df3-e509-4bc9-ad4b-5f77ad40da69",
            "23003df3-e509-4bc9-ad!@#,$%4b-5f77ad40da69",
            "                                        ",
            "    23003df3-e509-4bc9-ad4b-5f77ad40da69",
            "23003df3-e509-4bc9-ad4b-5f77ad40da69     ",
            "23003df3-e5 09-4 b c9-a d 4b-5f77  ad40da69"
    ])
    def test_get_image_invalid_id(self, image_obj, img_id):
        response = image_obj.get_image_by_id(img_id)

        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        try:
            BaseAssertion.assert_schema(response, models.NotFound)
        except json.JSONDecodeError:
            assert False, "The response body does not match the model!"

    def test_post_create_image_no_request_body(self, image_obj):
        request_body = None
        response = image_obj.create_image(request_body)

        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.PostBadRequest)

    def test_post_create_image_no_required_params(self, image_obj):
        request_body = {}
        response = image_obj.create_image(request_body)

        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.BadRequest)

    def test_post_create_image_invalid_params(self, image_obj):
        request_body = {
            'name111': 'qa-test-image1',
            'volume_id111': '43aff485-5154-499d-a8f1-e9efba93fc30'
        }

        response = image_obj.create_image(request_body)
        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.BadRequest)

    def test_post_create_image_not_exist_volume(self, image_obj):
        request_body = {
            'name': 'qa-test-image',
            'volume_id': '43aff485-5154-499d-a8f1-e9efba93fc309'
        }

        response = image_obj.create_image(request_body)
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    def test_delete_not_exist_image(self, image_obj):
        image_id = "23003df3-e509-4bc9-ad4b-5f77ad40da6910"
        response = image_obj.delete_image(image_id)
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)
