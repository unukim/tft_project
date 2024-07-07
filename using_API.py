import numpy as np
import pandas as pd
import requests
import time

#api_key = RGAPI-c66917e8-3a95-4d1e-9831-efe3e21b0d66
class load_data:

    def __init__(self, api_key):
        self.api_key = api_key
        self.request_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.api_key
        }
        self.base_url = "https://kr.api.riotgames.com/tft/"

