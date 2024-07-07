import requests

from helpers import get_api_key


class RIOT:
    def __init__(self, key):
        self.api_key = get_api_key("key.txt")
        self.base_url = "https://vn2.api.riotgames.com/tft/"


    def respone(self, queue):
        return requests.get()