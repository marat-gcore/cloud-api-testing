from typing import Type
from pydantic import BaseModel, ValidationError
from logs.custom_errors import CodeLogMsg


class BaseAssertion:
    @staticmethod
    def assert_status_code(response, expected_code):
        assert response.status_code == expected_code, CodeLogMsg(response) \
            .add_compare_result(response.status_code, expected_code) \
            .add_request_info() \
            .add_response_info() \
            .get_message()

    @staticmethod
    def assert_schema(response, model: Type[BaseModel]):
        body = response.json()
        if isinstance(body, list):
            for item in body:
                model.model_validate(item, strict=True)
        else:
            model.model_validate(body, strict=True)

    @staticmethod
    def assert_obj_found(response_body, request_key, request_value):
        if response_body['count'] > 0:
            obj_found = False
            for item in response_body['results']:
                if request_value == item.get(request_key):
                    obj_found = True
                    return item.get("id")
            if not obj_found:
                print("The object was not created")
                raise ValidationError
        else:
            print("The object was not created")
            raise ValidationError
