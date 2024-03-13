from typing import List, Dict, Optional
from pydantic import BaseModel


class Image(BaseModel):
    metadata: Dict[str, str]
    visibility: str
    os_type: str
    created_at: str
    ssh_key: str
    name: str
    project_id: int
    os_version: Optional[str] = None
    architecture: str
    min_ram: int
    hw_machine_type: Optional[str] = None
    status: str
    id: str
    updated_at: str
    region_id: int
    disk_format: str
    region: str
    metadata_detailed: List[str] = None
    display_order: int
    os_distro: str
    size: int
    min_disk: int


class RequestSuccessful(BaseModel):
    tasks: List[str]


class PostBadRequest(BaseModel):
    exception_class: str
    message: str
    request_id: str


class NotFound(BaseModel):
    exception_class: str
    message: str
    request_id: str


class BadRequest(NotFound):
    invalid_fields: Dict[str, list]


class ImageWithPrice(Image):
    price_per_month: float
    price_per_hour: float
    price_status: str
    currency_code: str


class ListImages(BaseModel):
    count: int
    results: List[dict]

