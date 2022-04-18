from .device import Device
from .group import Group
from .user import User
from .announcement import AllAnnouncements
from app.controllers.ssh_ps import RemoteShell


class MDM:
    def __init__(self) -> None:
        pass

    def get_device(self, device_id):
        from .base_api import get

        device = get(f"devices/{device_id}")
        if not device:
            return None
        return Device.parse_obj(device)

    @property
    def devices(self) -> list[Device]:
        from .base_api import get_list_of

        devices = get_list_of("devices", "devices")
        return [Device.parse_obj(data) for data in devices]

    @property
    def groups(self) -> list[Group]:
        from .base_api import get_list_of

        groups_data = get_list_of("groups", "groups")
        return [Group.parse_obj(data) for data in groups_data]

    @property
    def users(self):
        from .base_api import get_list_of

        users = get_list_of("users", "users")
        return [User.parse_obj(user) for user in users]

    def __getitem__(self, device_id: int or str) -> Device or None:
        for device in self.devices:
            if type(device_id) == str:
                if device.imei and device_id in device.imei:
                    return device
            else:
                if int(device.id) == device_id:
                    return device

    def sync(self, is_full_sync=True):
        from .base_api import post

        # https://mdm.kryptr.li:9383/api/v1/mdm/directory/sync
        # POST: {is_full_sync: true}
        post("directory/sync", data=dict(is_full_sync=is_full_sync))

    @property
    def announcements(self):
        from .base_api import get

        data = get("announcements")
        all = AllAnnouncements.parse_obj(data)
        return all.announcement

    def get_group_by_name(self, group_name: str) -> Group:
        for group in self.groups:
            if group_name.lower() == group.name.lower():
                return group

    @property
    def shell(self) -> RemoteShell:

        return RemoteShell()
