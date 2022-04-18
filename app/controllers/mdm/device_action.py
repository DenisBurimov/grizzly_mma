from .base_api import post, get, delete


class DeviceAction(object):
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name

    @property
    def status(self):
        status = get(f"devices/{self.device_id}/actions/{self.name}")
        return status["status_description"] if "status_description" in status else None

    def run(self, data: dict = None, **kwargs):
        return post(f"devices/{self.device_id}/actions/{self.name}", data, **kwargs)

    def remove_retired(self, data: dict = None, **kwargs):
        return delete("devices/actions/remove", data, **kwargs)

    def cancel(self):
        pass

    def __repr__(self) -> str:
        return f"{self.device_id}:{self.name}"
