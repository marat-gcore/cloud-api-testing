from typing import Optional
from pydantic import BaseModel, Field


class Image(BaseModel):
    metadata: dict[str, str]
    visibility: str
    os_type: Optional[str] = None
    created_at: str
    ssh_key: Optional[str] = None
    name: str
    project_id: int
    os_version: Optional[str] = None
    architecture: str
    min_ram: int = Field(ge=0)
    hw_machine_type: Optional[str] = None
    hw_firmware_type: Optional[str] = None
    status: str
    id: str
    updated_at: str
    region_id: int
    disk_format: str
    region: str
    metadata_detailed: list[dict] = None
    display_order: Optional[int] = None
    os_distro: Optional[str] = None
    size: int
    min_disk: int = Field(ge=0)


class RequestSuccessful(BaseModel):
    tasks: list[str]


class PostBadRequest(BaseModel):
    exception_class: str
    message: str
    request_id: str


class NotFound(BaseModel):
    exception_class: str
    message: str
    request_id: str


class BadRequest(NotFound):
    invalid_fields: dict[str, list]


class ImageWithPrice(Image):
    price_per_month: float
    price_per_hour: float
    price_status: str
    currency_code: str


class ListImages(BaseModel):
    count: int = Field(ge=0)
    results: list[dict] | None

