from api.api_client import APIClient


class ImagesRequests(APIClient):
    IMAGES = f"/v1/images"

    def get_images(self, project_id, region_id, params=None):
        return self.get_obj(
            endpoint=f"{self.IMAGES}/{project_id}/{region_id}",
            headers=self.session.headers,
            params=params
        )

    def get_image_by_id(self, project_id, region_id, obj_id, params=None):
        return self.get_obj(
            endpoint=f"{self.IMAGES}/{project_id}/{region_id}/{obj_id}",
            headers=self.session.headers,
            params=params
        )

    def create_image(self, project_id, region_id, request_body):
        return self.post_obj(
            endpoint=f"{self.IMAGES}/{project_id}/{region_id}",
            headers=self.session.headers,
            json=request_body
        )

    def update_image(self, project_id, region_id, obj_id, request_body):
        return self.patch_obj(
            endpoint=f"{self.IMAGES}/{project_id}/{region_id}/{obj_id}",
            headers=self.session.headers,
            json=request_body
        )

    def delete_image(self, project_id, region_id, obj_id):
        return self.delete_obj(
            endpoint=f"{self.IMAGES}/{project_id}/{region_id}/{obj_id}",
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
