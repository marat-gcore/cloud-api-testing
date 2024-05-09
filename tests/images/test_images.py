import pytest
import time
import logging

from http import HTTPStatus
from assertions.assertion_base import BaseAssertion
from models.images import images_models as models

logger = logging.getLogger("logger_tests")


class TestImages:
    """
    /v1/images/<project_id>/<region_id>
    """

    # -------positive-------

    # @pytest.mark.skip
    def test_get_list_images(self, client_images, project_id, region_id):
        response = client_images.get_images(project_id=project_id, region_id=region_id)

        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.ListImages)
        if len(response.json()["results"]) > 0:
            BaseAssertion.assert_schema(response.json()["results"], models.Image)

    # @pytest.mark.skip
    @pytest.mark.parametrize("params", ['private', 'public', 'shared'])
    def test_get_list_images_by_visibility_param(self, client_images, project_id, region_id, params):
        query_param = {'visibility': f'{params}'}
        response = client_images.get_images(
            project_id=project_id,
            region_id=region_id,
            params=query_param
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        if len(response.json()["results"]) > 0:
            for item in response.json()['results']:
                assert item['visibility'] == f'{params}'

    # @pytest.mark.skip
    def test_post_create_image(self, client_images, create_img, image_id):
        BaseAssertion.assert_status_code(create_img, HTTPStatus.OK)
        BaseAssertion.assert_schema(create_img, models.RequestSuccessful)

    # @pytest.mark.skip
    def test_get_image_by_id(self, client_images, project_id, region_id, image_id):
        response = client_images.get_image_by_id(
            project_id=project_id,
            region_id=region_id,
            obj_id=image_id
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.Image)

    # @pytest.mark.skip
    def test_patch_update_image(self, client_images, img_request_body, image_id, project_id, region_id):
        request_body = {
            'name': 'qa-img-changed'
        }
        request_key = 'name'
        request_value = request_body.get(request_key)

        response = client_images.update_image(
            project_id=project_id,
            region_id=region_id,
            obj_id=image_id,
            request_body=request_body
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.Image)
        time.sleep(2)

        response = client_images.get_image_by_id(
            project_id=project_id,
            region_id=region_id,
            obj_id=image_id
        )
        response_body = response.json()
        assert request_value == response_body.get(request_key)

    # @pytest.mark.skip
    def test_delete_image(self, client_images, image_id, project_id, region_id):
        response = client_images.delete_image(
            project_id=project_id,
            region_id=region_id,
            obj_id=image_id
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.OK)
        BaseAssertion.assert_schema(response, models.RequestSuccessful)
        time.sleep(2)

        response = client_images.get_image_by_id(
            project_id=project_id,
            region_id=region_id,
            obj_id=image_id
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    # -------negative-------

    # @pytest.mark.skip
    def test_get_list_images_invalid_visibility_param(self, client_images, project_id, region_id):
        query_param = {'visibility': 'somevalue'}
        response = client_images.get_images(
            project_id=project_id,
            region_id=region_id,
            params=query_param
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.BadRequest)

    # @pytest.mark.skip
    def test_get_image_not_exist_id(self, client_images, project_id, region_id):
        image_id = "23003df3-e509-4bc9-ad4b-5f77ad40da691"
        response = client_images.get_image_by_id(
            project_id=project_id,
            region_id=region_id,
            obj_id=image_id
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    # @pytest.mark.skip
    def test_post_create_image_no_request_body(self, client_images, project_id, region_id):
        request_body = None
        response = client_images.create_image(
            project_id=project_id,
            region_id=region_id,
            request_body=request_body
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.PostBadRequest)

    # @pytest.mark.skip
    def test_post_create_image_no_required_params(self, client_images, project_id, region_id):
        request_body = {}
        response = client_images.create_image(
            project_id=project_id,
            region_id=region_id,
            request_body=request_body
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.BAD_REQUEST)
        BaseAssertion.assert_schema(response, models.BadRequest)

    # @pytest.mark.skip
    def test_post_create_image_not_exist_volume(self, client_images, project_id, region_id):
        request_body = {
            'name': 'qa-test-image',
            'volume_id': 'fbfb26d1-37d9-4bd9-82f6-e1d0fd3091c89'
        }

        response = client_images.create_image(
            project_id=project_id,
            region_id=region_id,
            request_body=request_body
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    # @pytest.mark.skip
    def test_patch_not_exist_id(self, client_images, img_request_body, project_id, region_id):
        img_id = "9726377c-2991-45be-8fce-ff9521cae512"

        response = client_images.update_image(
            project_id=project_id,
            region_id=region_id,
            obj_id=img_id,
            request_body=img_request_body
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)

    # @pytest.mark.skip
    def test_delete_not_exist_image(self, client_images, project_id, region_id):
        img_id = "9726377c-2991-45be-8fce-ff9521cae512"

        response = client_images.delete_image(
            project_id=project_id,
            region_id=region_id,
            obj_id=img_id
        )
        BaseAssertion.assert_status_code(response, HTTPStatus.NOT_FOUND)
        BaseAssertion.assert_schema(response, models.NotFound)
