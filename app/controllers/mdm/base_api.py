import json
from urllib.parse import urljoin

import requests

from config import BaseConfig

BASE_URL = BaseConfig.BASE_MDM_API_URL
API_KEY = BaseConfig.MDM_API_KEY


def get(sub_url, **kwargs) -> dict:
    url = urljoin(BASE_URL, sub_url)
    response = requests.get(url, headers={"Authorization": API_KEY}, **kwargs)
    return response.json()


def post(sub_url, data: dict = None, **kwargs) -> int:
    url = urljoin(BASE_URL, sub_url)
    response = requests.post(
        url, headers={"Authorization": API_KEY}, json=data, **kwargs
    )
    return response.status_code


def put(sub_url, data: dict = None, **kwargs) -> int:
    url = urljoin(BASE_URL, sub_url)
    response = requests.put(
        url, headers={"Authorization": API_KEY}, json=data, **kwargs
    )
    return response.status_code


def delete(sub_url, data: dict = None, **kwargs) -> int:
    url = urljoin(BASE_URL, sub_url)
    response = requests.delete(
        url, headers={"Authorization": API_KEY}, json=data, **kwargs
    )
    return response.status_code


def get_list_of(name, sub_url, **kwargs):
    result = get(sub_url, **kwargs)
    if name not in result:
        return []
    collection = result[name]
    if "paging" in result:
        while "next" in result["paging"]:
            next_url = result["paging"]["next"]
            response = requests.get(
                next_url, headers={"Authorization": API_KEY}, **kwargs
            )
            response.raise_for_status()
            result = json.loads(response.text)
            collection += result[name]
    return collection
