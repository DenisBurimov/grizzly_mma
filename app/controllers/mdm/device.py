from datetime import datetime
from typing import Optional, Any, Union
from pydantic import BaseModel, Field

from .base_api import get_list_of
from .device_action import DeviceAction
from .user import User

DEPROVISION = "deprovision"
REMOVE = "REMOVE"


class DevicePrivacySettings(BaseModel):
    view_privacy_settings: Optional[bool]
    disable_wipe: Optional[int]
    device_name_pattern: Optional[str]
    device_state_report: Optional[int]
    fetch_phone_number: Optional[int]
    fetch_location: Optional[int]
    fetch_device_name: Optional[int]
    fetch_installed_app: Optional[int]
    disable_bug_report: Optional[int]
    fetch_user_installed_certs: Optional[int]
    fetch_mac_address: Optional[int]
    recent_users_report: Optional[int]
    disable_remote_control: Optional[int]
    disable_clear_passcode: Optional[int]


class DeviceLocationSettings(BaseModel):
    location_services: Optional[int]
    is_location_history_enabled: Optional[int]
    tracking_status: Optional[int]
    location_tracking_status: Optional[int]
    location_history_duration: Optional[int]
    location_interval: Optional[int]
    location_radius: Optional[int]


class DeviceNetworkUsage(BaseModel):
    outgoing_network_usage: Optional[float]
    device_id: Optional[int]
    incoming_wifi_usage: Optional[float]
    outgoing_wifi_usage: Optional[float]
    incoming_network_usage: Optional[float]


class DeviceSim(BaseModel):
    is_roaming: Optional[bool]
    device_id: Optional[int]
    current_carrier_network: Optional[str]
    current_mnc: Optional[str]
    subscriber_mnc: Optional[str]
    imsi: Optional[str]
    slot: Optional[int]
    label: Optional[str]
    subscriber_carrier_network: Optional[str]
    iccid: Optional[str]
    sim_id: Optional[int]
    carrier_setting_version: Optional[str]
    imei: Optional[int]
    phone_number: Optional[str]
    subscriber_mcc: Optional[str]
    current_mcc: Optional[str]
    label_id: Optional[str]


class DeviceNetwork(BaseModel):
    is_personal_hotspot_enabled: Optional[bool]
    is_roaming: Optional[bool]
    device_id: Optional[int]
    voice_roaming_enabled: Optional[bool]
    current_carrier_network: Optional[str]
    current_mnc: Optional[str]
    subscriber_mnc: Optional[str]
    ethernet_ip: Optional[str]
    data_roaming_enabled: Optional[bool]
    ethernet_macs: Optional[str]
    subscriber_carrier_network: Optional[str]
    wifi_ip: Optional[str]
    iccid: Optional[str]
    bluetooth_mac: Optional[str]
    carrier_setting_version: Optional[str]
    wifi_mac: Optional[str]
    phone_number: Optional[str]
    subscriber_mcc: Optional[str]
    current_mcc: Optional[str]


class DeviceSecurity(BaseModel):
    play_protect: Optional[bool]
    safetynet_availabiity: Optional[bool]
    external_storage_encryption: Optional[int]
    device_id: Optional[int]
    storage_encryption: Optional[bool]
    safetynet_cts: Optional[bool]
    safetynet_basic_integrity: Optional[bool]
    hardware_encryption_caps: Optional[int]
    efrp_status: Optional[int]
    device_rooted: Optional[bool]
    passcode_present: Optional[bool]
    efrp_account_details: Optional[list[Any]]
    passcode_complaint: Optional[bool]
    passcode_complaint_profiles: Optional[bool]
    safetynet_advice: Optional[str]


class DeviceKnoxDetails(BaseModel):
    knox_version: Optional[int]
    container_state: Optional[int]
    container_status: Optional[int]
    container_remarks: Optional[str]
    container_last_updated_time: Optional[int]


class DeviceOS(BaseModel):
    platform_type: Optional[int]
    device_id: Optional[int]
    build_version: Optional[str]
    os_version: Optional[int]
    os_name: Optional[str]


class DeviceDetails(BaseModel):
    agent_version_code: Optional[str]
    meid: Optional[str]
    warranty_number: Optional[str]
    cellular_technology: Optional[int]
    used_device_space: Optional[float]
    is_profileowner: Optional[bool]
    is_ios_native_app_registered: Optional[bool]
    office: Optional[str]
    remote_settings_enabled: Optional[bool]
    google_play_service_id: Optional[str]
    branch: Optional[str]
    apn_username: Optional[str]
    model_name: Optional[str]
    platform_type: Optional[int]
    registered_time: Optional[datetime]
    warranty_expiration_date: Optional[datetime]
    purchase_order_number: Optional[str]
    model: Optional[str]
    purchase_type: Optional[str]
    asset_tag: Optional[str]
    device_id: Optional[int]
    available_device_capacity: Optional[float]
    available_ram_memory: Optional[float]
    owned_by: Optional[int]
    warranty_type: Optional[str]
    product_name: Optional[str]
    agent_type: Optional[int]
    purchase_price: Optional[float]
    privacy_settings: Optional[DevicePrivacySettings]
    purchase_date: Optional[datetime]
    device_capacity: Optional[float]
    managed_status: Optional[int]
    processor_type: Optional[str]
    added_time: Optional[datetime]
    location_settings: Optional[DeviceLocationSettings]
    is_mail_server_enabled: Optional[bool]
    network_usage: Optional[DeviceNetworkUsage]
    eas_device_identifier: Optional[str]
    notification_service_type: Optional[int]
    description: Optional[str]
    sims: Optional[list[DeviceSim]]
    is_lost_mode_enabled: Optional[bool]
    is_knox_enabled: Optional[bool]
    network: Optional[DeviceNetwork]
    manufacturer: Optional[str]
    device_name: Optional[str]
    security: Optional[DeviceSecurity]
    lost_mode_status: Optional[int]
    knox_details: Optional[DeviceKnoxDetails]
    is_multiuser: Optional[bool]
    asset_owner: Optional[str]
    udid: Optional[str]
    last_contact_time: Optional[str]
    apn_password: Optional[str]
    battery_level: Optional[float]
    os: Optional[DeviceOS]
    build_version: Optional[str]
    is_supervised: Optional[bool]
    os_version: Optional[int]
    model_type: Optional[int]
    serial_number: Optional[str]
    model_id: Optional[int]
    agent_version: Optional[str]
    areamanager: Optional[str]
    total_ram_memory: Optional[float]
    imei: Optional[str]
    os_name: Optional[str]
    location: Optional[str]
    last_scan_time: Optional[datetime]
    user: Optional[User]
    remarks: Optional[str]
    unregistered_time: Optional[int]


class Device(BaseModel):
    managed_status: int
    id: Optional[int] = Field(alias="device_id")
    is_supervised: Optional[bool]
    os_version: Optional[str]
    is_lost_mode_enabled: Optional[bool]
    serial_number: Optional[str]
    device_type: Optional[int]
    owned_by: Optional[int]
    is_removed: Optional[bool]
    product_name: Optional[str]
    name: Optional[str] = Field(alias="device_name")
    platform_type: Optional[str]
    model: Optional[str]
    customer_name: Optional[str]
    customer_id: Optional[int]
    udid: Optional[str]
    last_contact_time: Optional[datetime]
    platform_type_id: Optional[int]
    user: Optional[User]
    device_capacity: Optional[float]
    imei: Optional[Union[list[str], str]]

    @property
    def actions(self) -> list:
        actions = get_list_of("actions", f"devices/{self.id}/actions")
        return [(action["name"], action["localized_name"]) for action in actions]

    def action(self, name):
        for short_name, full_name in self.actions:
            if name in (short_name, full_name):
                return DeviceAction(device_id=self.id, name=short_name)
            if name == DEPROVISION:
                return DeviceAction(device_id=self.id, name=DEPROVISION)
            if name == REMOVE:
                return DeviceAction(device_id=self.id, name=REMOVE)

    def wipe(self, wipe_sd_card=False):
        # a.run(data=dict(wipe_sd_card=False), params={"SUBREQUEST": "XMLHTTP"})
        action = self.action("complete_wipe")
        if action:
            # return action.run(data=dict(wipe_sd_card=wipe_sd_card), params={"SUBREQUEST": "XMLHTTP"})
            return action.run(data=dict(wipe_sd_card=wipe_sd_card))

    def deprovision(self):
        """Method which first wipe and send device to "retired" section
        and if status code is ok, remove device from retired section"""

        action = self.action(DEPROVISION)
        if action:
            response_status_code = action.run(data=dict(wipe_reason="3"))
            if response_status_code == 200:
                return self.remove_from_mdm()
            else:
                return response_status_code

    def remove_from_mdm(self):
        """Method for removing device from retired section
        Using DELETE method and takes dict as argument
        with device_ids as key and list of id's to be removed as value"""

        action = self.action(REMOVE)
        if action:
            return action.remove_retired(data=dict(device_ids=[str(self.id)]))

    def __repr__(self) -> str:
        return f"\n{self.id}:{self.model}:{self.serial_number}:{self.imei}"
