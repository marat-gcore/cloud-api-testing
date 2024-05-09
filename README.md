## List of tests

### Images

---

*Positive*

- test_get_list_images
- test_get_list_images_by_visibility_param
- test_post_create_image
- test_get_image_by_id
- test_patch_update_image
- test_delete_image

*Negative*

- test_get_list_images_invalid_visibility_param
- test_get_image_not_exist_id
- test_post_create_image_no_request_body
- test_post_create_image_no_required_params
- test_post_create_image_not_exist_volume
- test_patch_not_exist_id
- test_delete_not_exist_image 