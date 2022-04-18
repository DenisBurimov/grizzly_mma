from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from .group import Group, GroupType
from .device import Device

# from .base_api import post, put, delete, get

from app.logger import log

DETAIL_MESSAGE_FORMAT = "<pre>{message}</pre>"
DETAIL_MESSAGE_FORMAT_EX = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" content="user-scalable=0" />
    <meta forua="true" content="no-cache" http-equiv="Cache-Control"/>
    <meta name="apple-mobile-web-app-capable" content="yes"/>
    <meta name="HandheldFriendly" content="true"/>
    <meta name="MobileOptimized" content="width"/>
  </head>
  <body>
    {message}
  </body>
</html>"""

DEFAULT_ICON = "/images/announcement/nbaricon/alert.png"
ALERT_ICON = "/images/announcement/nbaricon/alert.png"
INFO_ICON = "/images/announcement/nbaricon/info.png"
WARNING_ICON = "/images/announcement/nbaricon/warning.png"
ANNOUNCEMENT_ICON = "/images/announcement/nbaricon/announcement.png"

DEFAULT_TITLE_COLOR = "#ffffff"
EXCLUDE_FIELDS = {"create", "modify", "delete", "distribute", "set_message"}

MAP_ICON = dict(
    alert=ALERT_ICON,
    warning=WARNING_ICON,
    announcement=ANNOUNCEMENT_ICON,
    info=INFO_ICON,
)

DEFAULT_LEVEL = "announcement"


class AnnouncementDetail(BaseModel):
    title_color: Optional[str] = DEFAULT_TITLE_COLOR
    title: str
    nbar_icon: Optional[str] = DEFAULT_ICON
    nbar_message: Optional[str]
    detail_message: Optional[str]
    needs_acknowledgement: Optional[bool] = False
    ack_button: Optional[str] = ""


class Announcement(BaseModel):
    name: str = Field(alias="announcement_name")
    creation_time: Optional[datetime]
    last_modified_time: Optional[datetime]
    format: int = Field(alias="announcement_format", default=1)
    needs_acknowledgement: Optional[bool]
    last_modified_by_user: Optional[str]
    created_by_user: Optional[str]
    collection_id: Optional[int]
    ack_button: Optional[str]
    is_moved_to_trash: Optional[bool]
    profile_id: Optional[int]
    id: Optional[int] = Field(alias="announcement_id")
    detail: Optional[AnnouncementDetail] = Field(alias="announcement_detail")

    class Config:
        allow_population_by_field_name = True

    def create(self) -> bool:
        from .base_api import post

        data = self.dict(by_alias=True, exclude_none=True)
        status = post("announcements", data)
        return 200 == status

    def modify(self):
        from .base_api import put

        data = self.dict(
            by_alias=True, exclude_none=True, include={"name", "detail", "format"}
        )
        status = put(f"announcements/{self.id}", data)
        return 204 == status

    def delete(self):
        from .base_api import delete

        status = delete(f"announcements/{self.id}")
        return 204 == status

    @staticmethod
    def get(announcement_id: int):
        from .base_api import get

        data = get(f"announcements/{announcement_id}")
        if "error_description" in data:
            log(
                log.ERROR,
                "Announcement.get(%s): [%s]",
                announcement_id,
                data["error_description"],
            )
            return None
        return Announcement.parse_obj(data)

    def send_to_groups(self, groups: list[Group]):
        from .base_api import post

        data = dict(group_ids=[g.id for g in groups])
        status = post(f"announcements/{self.id}/groups", data)
        return 204 == status

    def send_to_group_by_name(self, group_name: str):
        from .mdm import MDM

        mdm = MDM()
        for group in mdm.groups:
            if group_name == group.name:
                if group.type == GroupType.USER_GROUP:
                    user_ids = [u.user_id for u in group.members]
                    return self.send_to_devices(
                        [
                            d
                            for d in mdm.devices
                            if d.user and d.user.user_id in user_ids
                        ]
                    )
                else:
                    return self.send_to_groups([group])
        log(
            log.ERROR,
            "Announcement.send_to_group_by_name cannot found group name: [%s]",
            group_name,
        )

    def send_to_devices(self, devices: list[Device]):
        from .base_api import post

        data = dict(device_ids=[d.id for d in devices])
        status = post(f"announcements/{self.id}/devices", data)
        return 204 == status

    def set_message(self, value: str):
        self.detail.nbar_message = value
        self.detail.detail_message = DETAIL_MESSAGE_FORMAT.format(message=value)

    def set_level(self, value: str):
        if value in MAP_ICON:
            self.detail.nbar_icon = MAP_ICON[value]
        else:
            log(log.ERROR, "Announcement.set_level: wrong value: [%s]", value)
            self.detail.nbar_icon = DEFAULT_ICON

    def get_level(self):
        for value in MAP_ICON:
            if self.detail.nbar_icon == MAP_ICON[value]:
                return value
        return DEFAULT_LEVEL

    def __repr__(self):
        return f"{self.id}:{self.name}"


class AllAnnouncements(BaseModel):
    metadata: dict
    delta_token: Optional[str] = None
    announcement: list[Announcement]
