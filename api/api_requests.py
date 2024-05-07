from api.api_client import APIClient


# class BaseRequests:
#     def __init__(self, client, bearer_token):
#         self.__client = client.session
#         self.__bearer_token = bearer_token
#         self.__headers = {'Authorization': f"Bearer {self.__bearer_token}"}
#         self.endpoint_images = Endpoints.IMAGES
#         self.endpoint_tasks = Endpoints.TASKS
#
#     def get_obj(self, endpoint, params):
#         return self.__client.get(url=endpoint, headers=self.__headers, params=params)
#
#     def post_obj(self, endpoint, **kwargs):
#         return self.__client.post(endpoint, headers=self.__headers, **kwargs)
#
#     def patch_obj(self, endpoint, **kwargs):
#         return self.__client.patch(endpoint, headers=self.__headers, **kwargs)
#
#     def delete_obj(self, endpoint):
#         return self.__client.delete(endpoint, headers=self.__headers)


class ImagesRequests(APIClient):
    def get_images(self, params=None):
        return self.get_obj(endpoint=self.IMAGES, headers=self.session.headers, params=params)

    def get_image_by_id(self, obj_id, params=None):
        return self.get_obj(endpoint=f"{self.IMAGES}/{obj_id}", headers=self.session.headers, params=params)

    def create_image(self, request_body):
        return self.post_obj(endpoint=self.IMAGES, headers=self.session.headers, json=request_body)

    def update_image(self, obj_id, request_body):
        return self.patch_obj(endpoint=f"{self.IMAGES}/{obj_id}", headers=self.session.headers, json=request_body)

    def delete_image(self, obj_id):
        return self.delete_obj(endpoint=f"{self.IMAGES}/{obj_id}", headers=self.session.headers)


class TasksRequests(APIClient):
    def get_task_by_id(self, obj_id, params=None):
        return self.get_obj(endpoint=f"{self.TASKS}/{obj_id}", headers=self.session.headers, params=params)
