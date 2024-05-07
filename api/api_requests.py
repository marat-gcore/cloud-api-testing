from api.api_client import APIClient


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
