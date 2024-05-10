from api.api_client import APIClient


class ImagesRequests(APIClient):
    IMAGES = f"/v1/images"

    def __init__(self, base_url, token, project_id, region_id):
        super().__init__(base_url, token)
        self.project_id = project_id
        self.region_id = region_id
        self.endpoint = f"{self.IMAGES}/{self.project_id}/{self.region_id}"

    def get_images(self, params=None):
        return self.get_obj(
            endpoint=self.endpoint,
            headers=self.session.headers,
            params=params
        )

    def get_image_by_id(self, obj_id, params=None):
        return self.get_obj(
            endpoint=f"{self.endpoint}/{obj_id}",
            headers=self.session.headers,
            params=params
        )

    def create_image(self, request_body):
        return self.post_obj(
            endpoint=self.endpoint,
            headers=self.session.headers,
            json=request_body
        )

    def update_image(self, obj_id, request_body):
        return self.patch_obj(
            endpoint=f"{self.endpoint}/{obj_id}",
            headers=self.session.headers,
            json=request_body
        )

    def delete_image(self, obj_id):
        return self.delete_obj(
            endpoint=f"{self.endpoint}/{obj_id}",
            headers=self.session.headers
        )


class TasksRequests(APIClient):
    TASKS = "/v1/tasks"

    def get_task_by_id(self, obj_id, params=None):
        return self.get_obj(
            endpoint=f"{self.TASKS}/{obj_id}",
            headers=self.session.headers,
            params=params
        )
