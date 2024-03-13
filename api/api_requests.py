from api import api_endpoints


class BaseRequests:
    def __init__(self, client, bearer_token):
        self.client = client
        self.bearer_token = bearer_token

    def get_obj(self, endpoint, params):
        headers = {'Authorization': f"Bearer {self.bearer_token}"}
        return self.client.get(endpoint, headers=headers, params=params)

    def post_obj(self, endpoint, **kwargs):
        headers = {'Authorization': f"Bearer {self.bearer_token}"}
        return self.client.post(endpoint, headers=headers, **kwargs)

    def patch_obj(self, endpoint, **kwargs):
        headers = {'Authorization': f"Bearer {self.bearer_token}"}
        return self.client.patch(endpoint, headers=headers, **kwargs)

    def delete_obj(self, endpoint):
        headers = {'Authorization': f"Bearer {self.bearer_token}"}
        return self.client.delete(endpoint, headers=headers)


class ImagesRequests(BaseRequests):
    def get_images(self, params=None):
        endpoint = api_endpoints.ImagesEndpoints.IMAGES
        return self.get_obj(endpoint, params)

    def get_image_by_id(self, obj_id, params=None):
        endpoint = f"{api_endpoints.ImagesEndpoints.IMAGES}/{obj_id}"
        return self.get_obj(endpoint, params)

    def create_image(self, request_body):
        endpoint = api_endpoints.ImagesEndpoints.IMAGES
        return self.post_obj(endpoint, json=request_body)

    def update_image(self, obj_id, request_body):
        endpoint = f"{api_endpoints.ImagesEndpoints.IMAGES}/{obj_id}"
        return self.patch_obj(endpoint, json=request_body)

    def delete_image(self, obj_id):
        endpoint = f"{api_endpoints.ImagesEndpoints.IMAGES}/{obj_id}"
        return self.delete_obj(endpoint)
