from api.api_endpoints import Endpoints


class BaseRequests:
    def __init__(self, client, bearer_token):
        self.__client = client
        self.__bearer_token = bearer_token
        self.__headers = {'Authorization': f"Bearer {self.__bearer_token}"}
        self.endpoint_images = Endpoints.IMAGES
        self.endpoint_tasks = Endpoints.TASKS

    def get_obj(self, endpoint, params):
        return self.__client.get(endpoint, headers=self.__headers, params=params)

    def post_obj(self, endpoint, **kwargs):
        return self.__client.post(endpoint, headers=self.__headers, **kwargs)

    def patch_obj(self, endpoint, **kwargs):
        return self.__client.patch(endpoint, headers=self.__headers, **kwargs)

    def delete_obj(self, endpoint):
        return self.__client.delete(endpoint, headers=self.__headers)


class ImagesRequests(BaseRequests):
    def get_images(self, params=None):
        return self.get_obj(self.endpoint_images, params)

    def get_image_by_id(self, obj_id, params=None):
        return self.get_obj(f"{self.endpoint_images}/{obj_id}", params)

    def create_image(self, request_body):
        return self.post_obj(self.endpoint_images, json=request_body)

    def update_image(self, obj_id, request_body):
        return self.patch_obj(f"{self.endpoint_images}/{obj_id}", json=request_body)

    def delete_image(self, obj_id):
        return self.delete_obj(f"{self.endpoint_images}/{obj_id}")


class TasksRequests(BaseRequests):
    def get_task_by_id(self, obj_id, params=None):
        return self.get_obj(f"{self.endpoint_tasks}/{obj_id}", params)
