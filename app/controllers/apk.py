from pydantic import BaseModel


class InitialUserCredentials(BaseModel):
    itemText: str
    type: str


def get_qrcode_public_key(string_data):
    qr_data = InitialUserCredentials.parse_raw(string_data)
    return qr_data.itemText
