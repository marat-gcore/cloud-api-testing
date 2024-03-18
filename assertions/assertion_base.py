from pydantic import TypeAdapter
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
    def assert_schema(response, schema):
        if isinstance(response, list):
            TypeAdapter(list[schema]).validate_python(response)
        else:
            schema.model_validate(response.json(), strict=True)

    @staticmethod
    def assert_obj_found(response, request_key, request_value):
        response_body = response.json()
        if response_body['count'] > 0:
            obj_found = False
            for item in response_body['results']:
                if request_value == item.get(request_key):
                    obj_found = True
                    return item.get("id")
            if not obj_found:
                assert False, "The object was not created"
        else:
            assert False, "The object was not created"
