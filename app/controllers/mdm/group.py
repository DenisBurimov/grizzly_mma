from enum import IntEnum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .device import DeviceDetails
from .user import User

from .base_api import get
from app.logger import log


class GroupType(IntEnum):
    DEVICE_GROUP = 6
    USER_GROUP = 7


class Group(BaseModel):
    created_time: datetime
    id: Optional[int] = Field(alias="group_id")
    name: str
    type: GroupType = Field(alias="group_type")
    member_count: int

    @property
    def members(self):
        # get ids
        data_members = get(f"groups/{self.id}/members")
        if data_members and "member_ids" in data_members:
            IS_USERS = self.type == GroupType.USER_GROUP
            MEMBER_CLASS = User if IS_USERS else DeviceDetails
            for id in data_members["member_ids"]:
                MEMBER_URL = f"users/{id}" if IS_USERS else f"devices/{id}"
                data = get(MEMBER_URL)
                if "error_code" in data:
                    log(log.DEBUG, "ErrorCode: [%s]", data["error_code"])
                    continue
                yield MEMBER_CLASS.parse_obj(data)


class Metadata(BaseModel):
    total_record_count: int


class Paging(BaseModel):
    next: str


class AllGroups(BaseModel):
    metadata: Metadata
    groups: list[Group]
    paging: Paging
