import requests

from helpers import get_api_key

m_linux_user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0"
m_macOs_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


class RIOT:
    def __init__(self, key):
        self.api_key = get_api_key("key.txt")
        self.request_header = {
            "User-Agent": m_linux_user_agent,
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.api_key
        }
        self.base_url = "https://vn2.api.riotgames.com/tft/"

